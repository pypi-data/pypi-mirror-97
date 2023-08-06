# -*- coding: utf-8 -*-

import inspect
import functools
import itertools

import asyncio
import aioredis

from .spi import RedisClient as RedisClientAPI

from ifconf import configure_module, config_callback, configure_main

import logging
logger = logging.getLogger(__name__)

@config_callback
def config(loader):
    loader.add_attr('redis_uri_main', 'redis://localhost:6379/0?encoding=utf-8', help='redis uri to connect') # or uri 'unix:///path/to/redis/socket?db=1'
    #loader.add_attr('redis_uri_logging', 'redis://localhost:6379/1?encoding=utf-8', help='redis uri to connect') # or uri 'unix:///path/to/redis/socket?db=1'


class RedisClient(RedisClientAPI):

    def __init__(self, loop):
        self.conf = configure_module(config)
        self.loop = loop
        self.conn = None
        self.conn_for_subscription = None
        self.count = 0
        self._subs = {}
        self._psubs = {}

    async def connect(self):
        self.conn = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=1)
        self.conn_for_subscription = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=2)
        #self.conn_for_logging = await aioredis.create_redis_pool(self.conf.redis_uri_logging, minsize=1, maxsize=1)
        #self.main_conn_shared = await aioredis.create_redis_pool(self.conf.redis_uri_main)
        #self.main_conn_exclusive = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=20)
        #self.logging_conn = await aioredis.create_redis_pool(self.conf.redis_uri_logging)
        #logger.notice('CONNECTED|URL=%s'.format(self.main_conn_shared.address))
        logger.notice('CONNECTED|URL=%s', self.conn.address)

    async def connect_for_blocking(self, minsize, maxsize):
        return await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=minsize, maxsize=maxsize)

    def execute_threadsafe(self, func, *args, **kwargs):
        #raw_result = self.loop.call_soon_threadsafe(functools.partial(self.conn.execute, cmd, *args))
        async def wrap():
            ret = func(*args, **kwargs)
            if inspect.isawaitable(ret):
                return await ret
            else:
                return ret
        coro = func(*args, **kwargs) if inspect.iscoroutinefunction(func) else wrap()
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        while True:
            try:
                ret = future.result(10)
            except asyncio.TimeoutError as e:
                logger.warn('REDIS_EXECUTE_THREADSAFE|TIMEOUT|FUTURE=%s', future)
                continue
            except Exception as e:
                logger.exception('REDIS_EXECUTE_THREADSAFE|ERROR=%s', e)
                ret = -1
                break
            else:
                break
        return ret

    async def execute(self, cmd, *args):
        return await self.conn.execute(cmd, *args, encoding=None)
            
    async def execute_str(self, cmd, *args):
        return await self.conn.execute(cmd, *args, encoding='UTF-8')
            
    async def subscribe(self, key):
        if key in self._subs:
            return self._subs[key]
        ch = await self.conn_for_subscription.subscribe(key)
        ch = ChannelForMultiConsumer(ch[0], self.loop)
        self._subs[key] = ch
        return ch
        
    async def unsubscribe(self, key_or_channel):
        if key_or_channel in self._subs:
            ch = self._subs[key_or_channel]
            if ch.unsubscribed():
                return await self.conn_for_subscription.unsubscribe(key_or_channel)
            else:
                return ch._channel
        else:
            return await self.conn_for_subscription.unsubscribe(key_or_channel)
        
    async def psubscribe(self, key):
        if key in self._psubs:
            return self._psubs[key]
        ch = await self.conn_for_subscription.psubscribe(key)
        ch = ChannelForMultiConsumer(ch[0], self.loop)
        self._psubs[key] = ch
        return ch
        
    async def punsubscribe(self, key_or_channel):
        if key_or_channel in self._psubs:
            ch = self._psubs[key_or_channel]
            if ch.unsubscribed():
                return await self.conn_for_subscription.punsubscribe(key_or_channel)
            else:
                return ch._channel
        else:
            return await self.conn_for_subscription.punsubscribe(key_or_channel)
        
    async def xadd(self, streamkey, *args, **kwargs):
        return await self.execute('XADD', streamkey, '*', *args, *itertools.chain.from_iterable(kwargs.items()))
        
    async def xadd_and_publish(self, pubkey, streamkey, *args, **kwargs):
        stream_id = await self.execute('XADD', streamkey, '*', *args, *itertools.chain.from_iterable(kwargs.items()))
        return await self.execute('PUBLISH', pubkey, stream_id)

    async def xget_str(self, streamkey, stream_id):
        ret = await self.execute_str('XREVRANGE', streamkey, stream_id, stream_id, 'COUNT', 1)
        return {v[0] : v[1] for v in zip(*[iter(ret[0][1])]*2)} if ret else {}

    async def xlast_str(self, streamkey):
        ret = await self.execute_str('XREVRANGE', streamkey, '+', '-', 'COUNT', 1)
        return {v[0] : v[1] for v in zip(*[iter(ret[0][1])]*2)} if ret else {}


    #https://github.com/aio-libs/aioredis/issues/310
    #https://github.com/aio-libs/aioredis/issues/369
    #https://github.com/aio-libs/aioredis/pull/373
    async def psub_and_xrange_str(self, subkey, streamkey, last_count = 0):
        logger.info("pubsub_channels=%s", self.conn_for_subscription.pubsub_channels())
        
        #ch = (await self.psubscribe(subkey))[0]
        ch = (await self.psubscribe(subkey))
        logger.info('PSUBSCRIBE|CHANNEL=%s', ch)
        last_id = '0'
        if last_count > 0:
            ret = await self.execute_str('XREVRANGE', streamkey, '+', '-', 'COUNT', last_count)
            for result in reversed(ret):
                last_id = result[0]
                yield {v[0] : v[1] for v in zip(*[iter(result[1])]*2)}
        async for msg in ch.iter():
            if msg is None:
                logger.info('PSUBSCRIBE|CHANNEL=%s|CLOSED', ch)
                break
            logger.info('PSUBSCRIBE|CHANNEL=%s|MSG=%s:%s', ch, msg[0], type(msg[1]))
            ret = await self.execute_str('XRANGE', streamkey, last_id+'1', '+')
            logger.info('XRANGE|STREAM=%s|LAST_ID=%s|ret=%s', streamkey, last_id, ret)
            if ret is None:
                continue
            for result in ret:
                last_id = result[0]
                yield {v[0] : v[1] for v in zip(*[iter(result[1])]*2)} 
        
    async def psub_and_xrange_str_for_each_id(self, subkey, streamkey):
        #ch = (await self.psubscribe(subkey))[0]
        ch = (await self.psubscribe(subkey))
        logger.debug('PSUBSCRIBE|CHANNEL=%s', ch)
        async for msg in ch.iter():
            logger.debug('PSUBSCRIBE|CHANNEL=%s|MSG=%s:%s', ch, msg[0], msg[1])
            ret = await self.execute_str('XRANGE', streamkey, msg[1], msg[1])
            logger.debug('XRANGE|STREAM=%s|ID=%s|RET=%s', streamkey, msg, ret)
            if ret is None:
                continue
            for result in ret:
                yield {v[0] : v[1] for v in zip(*[iter(result[1])]*2)}
            
    
    async def close(self):
        #to_close = [con for con in (self.conn_for_subscription, self.conn_for_logging, self.conn) if con != None]
        to_close = [con for con in (self.conn_for_subscription, self.conn) if con != None]
        [con.close() for con in to_close]
        await asyncio.gather(*[con.wait_closed() for con in to_close])

    '''
    async def blocking_command(self, coroutine):
        with await self.main_conn_exclusive as conn:
            await coroutine(conn)

    async def blocking_execute(self, cmd, *args):
        with await redis as r:
            await self.conn.execute(cmd, *args)

    
    async def get_and_wait(self, key):
        value = self.conn.get(key)
        if not value:
            ret = await conn.publish('test', key)
    '''

#https://github.com/aio-libs/aioredis/issues/310
#https://stackoverflow.com/questions/54159292/how-to-implement-single-producer-multi-consumer-with-aioredis-pub-sub
class ChannelForMultiConsumer:

    def __init__(self, channel, loop):
        self._future = None
        self._channel = channel
        self._loop = loop if not loop else asyncio.get_event_loop()
        self._count = 0

    def iter(self):
        return self

    def unsubscribed(self):
        self._count -= 1
        return self._count < 0
        
    def __aiter__(self):
        self._count += 1
        return self

    async def __anext__(self):
        if self._future:
            return await self._future
        self._future = self._loop.create_future()
        message = await self._channel.get()
        future, self._future = self._future, None
        future.set_result(message)
        return message

