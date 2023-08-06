#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
import time
from datetime import datetime, timedelta
from io import StringIO
from io import BytesIO
from collections import namedtuple
from enum import Enum
import hashlib

import importlib
import inspect
import functools

import msgpack
import json

import asyncio
import aiohttp
from aiohttp import web
import aiohttp_remotes
import aiofiles
import async_timeout
from http import HTTPStatus
import mimetypes

from ifconf import configure_module, config_callback

from .context import ServerContext
from .auth import Auth
from .spi import Event, EventSession
from .event import HandleType

import logging
        
@config_callback
def config(loader):
    loader.add_attr_boolean('behind_nginx', False, help='True if use ducts behind nginx')
    loader.add_attr('httpd_addr', '0.0.0.0', help='inet address to bind')
    loader.add_attr_int('httpd_port', 8080, help='inet port to bind')
    loader.add_attr_path('local_path_static', Path('./htdocs'), help='local path for static root')
    loader.add_attr_path('local_path_libs', Path('./libs'), hidden=True, help='local path for html/javascript files')

    loader.add_attr_path('module_path_libs', Path('./libs'), hidden=True, help='module path for html/javascript files')
    loader.add_attr_list('web_lib_file_extensions', ['.js', '.html', '.css'], hidden=True, help='web library file extensions')
    loader.add_attr_path('module_path_jsonp_template', Path('./assets/jsonp_template.js'), hidden=True, help='')
    loader.add_attr_path('module_path_favicon', Path('./assets/favicon.ico'), hidden=True, help='')
    
    loader.add_attr('root_path_ducts', '/ducts/', help='URL path for all path')
    loader.add_attr('root_path_static', '/static/', hidden=True, help='URL path for static_root')
    loader.add_attr('root_path_favicon', '/favicon.ico', hidden=True, help='')
    loader.add_attr('relative_path_libs_dir', 'libs', hidden=True, help='URL path for html/javascript files')
    loader.add_attr('relative_path_web_service_discovery', 'wsd', hidden=True, help='where web service discovery is located')
    loader.add_attr('relative_path_web_service_main_jsonp', 'main', hidden=True, help='where main web service is located')
    loader.add_attr('relative_path_event_spec', 'events.json', hidden=True, help='where event descriptions json is located')
    loader.add_attr('relative_path_api', 'api/v1/', hidden=True, help='')
    loader.add_attr('relative_path_websocket', 'ws/v1', hidden=True, help='')
    loader.add_attr('api_path_event', 'event', hidden=True, help='')
    loader.add_attr('api_path_event_id', 'event/{event_id}', hidden=True, help='')
    loader.add_attr('jsonp_callback_query', 'callback', hidden=True, help='')
    loader.add_attr('jsonp_callback_default', 'callback', hidden=True, help='')

    
@config_callback('web_service_discovery')
def wsd_config(loader):
    loader.add_attr('websocket_host', '{ws_host}', help='')
    loader.add_attr('websocket_url', '{ws_scheme}://{ws_host}{root_path_websocket}{session_id}', help='')
    loader.add_attr('websocket_url_reconnect', '{ws_scheme}://{ws_host}{root_path_websocket}{session_id}/reconnect', help='')
    loader.add_attr('api_host', '{api_host}', help='')
    loader.add_attr('api_url_root', '{api_scheme}://{api_host}{root_path_api}', help='')
    loader.add_attr('api_url_event', '{api_scheme}://{api_host}{root_path_api}{api_path_event}', help='')

@config_callback('web_socket_server')
def wsserver_config(loader):
    loader.add_attr_int('ping_pong_interval', 3, help='interval to send ping msg after pong msg received')
    loader.add_attr_int('reconnect_timeout', 60, help='wait timeout until reconnect')

    
class HttpdServer(object):

    def __init__(self, loop):
        self.logger = logging.getLogger(__name__).getChild('httpd')
        self.conf = configure_module(config)
        self.root_path_ducts = Path(self.conf.root_path_ducts)
        self.wsd = configure_module(wsd_config)
        self.wsd_dict = self.wsd._asdict()
        self.context = ServerContext(loop)
        with open(self.context.module_path(self.conf.module_path_jsonp_template), 'r') as f:
            self.jsonp_template = f.read()
        with open(self.context.module_path(self.conf.module_path_favicon), 'rb') as f:
            self.favicon = f.read()
        self.wss = WebSocketServer(self.context)
        self.app = web.Application(loop=self.context.loop)
        self.md5 = hashlib.md5()

    async def setup(self):
        await self.context.setup()
        self.setup_route()
        
    def _root_path_for(self, path, is_dir = False):
        return str(self.root_path_ducts.joinpath(path)) + ('/' if is_dir else '')

    def _root_path_for_websocket(self):
        return self._root_path_for(self.conf.relative_path_websocket, True)
        
    def _root_path_for_api(self):
        return self._root_path_for(self.conf.relative_path_api, True)
        
    def _root_path_for_libs(self):
        return self._root_path_for(self.conf.relative_path_libs_dir, True)
        
    def setup_route(self):
        self.app.router.add_static(self.conf.root_path_static, path=str(self.context.resolve_local_path(self.conf.local_path_static)), name='static', show_index=True)
        self.app.router.add_get(self.conf.root_path_favicon, lambda request: web.Response(body=self.favicon, content_type='image/x-icon'))
        for plugin, level in self.context.plugin_paths(self.conf.module_path_libs, self.conf.local_path_libs):
            for lib_file in [p for p in plugin.glob('**/*') if re.match('.*({})'.format('|'.join(self.conf.web_lib_file_extensions)),str(p))]:
                with open(lib_file, 'rb') as f:
                    buf = f.read()
                    self.md5.update(buf)
                    checksum = self.md5.hexdigest()
                    f = functools.partial((lambda src, mt, request : web.Response(body=src, content_type=mt, headers={'ETag':checksum})), buf, mimetypes.guess_type(str(lib_file))[0])
                self.app.router.add_get(self._root_path_for_libs() + lib_file.name, f)
        self.app.router.add_get(self._root_path_for_libs() + self.conf.relative_path_event_spec
                                , lambda request: web.json_response([s._asdict() for s in self.context.event_handler_manager.specs]))
        self.app.router.add_get(self._root_path_for(self.conf.relative_path_web_service_discovery), self.get_web_service_discovery)
        self.app.router.add_get(self._root_path_for(self.conf.relative_path_web_service_main_jsonp), self.get_web_service_main_jsonp)
        self.app.router.add_get(self._root_path_for_websocket()+'{session_id}', self.wss.websocket_handler)
        self.app.router.add_get(self._root_path_for_websocket()+'{session_id}/reconnect', self.wss.websocket_handler_reconnect)
        self.app.router.add_get(self._root_path_for_api()+self.conf.api_path_event, self.handle_event)
        self.app.router.add_get(self._root_path_for_api()+self.conf.api_path_event_id, self.handle_event_id)

    async def run(self):
        if self.conf.behind_nginx:
            await aiohttp_remotes.setup(self.app, aiohttp_remotes.XForwardedRelaxed())
        self.handler = self.app.make_handler()
        self.srv = await self.context.loop.create_server(self.handler, self.conf.httpd_addr, self.conf.httpd_port)
        self.logger.notice('START|SOCKET=%s', self.srv.sockets[0].getsockname())
        await self.context.run()

    async def close(self):
        self.logger.debug('CLOSEING|REDIS')
        await self.context.close()
        self.logger.debug('CLOSEING|HTTPD')
        self.srv.close()
        await self.srv.wait_closed()
        self.logger.debug('CLOSEING|APP')
        await self.app.shutdown()
        self.logger.debug('CLOSEING|HANDLERS')
        await self.handler.shutdown(60.0)
        self.logger.debug('CLEANING|APP')
        await self.app.cleanup()
        self.logger.debug('CLOSED')

    async def get_web_service_discovery(self, request):
        return web.json_response(await self._create_wsd_dict(request), status=HTTPStatus.OK.value)

    async def get_web_service_main_jsonp(self, request):
        params = request.rel_url.query
        callback = params.get(self.conf.jsonp_callback_query, self.conf.jsonp_callback_default)
        libs = self._root_path_for_libs()
        script = self.jsonp_template.replace('__TEMPLATE_DUCTS_LIBS__', libs).replace('__TEMPLATE_CALLBACK__', callback).replace('__TEMPLATE_WSD__', json.dumps(await self._create_wsd_dict(request)))
        res = web.Response(body=script, content_type='application/javascript')
        res.last_modified = datetime.now()
        return res
        
    async def handle_event(self, request):
        return web.json_response(self.context.event_handler_manager.key_ids)

    async def handle_event_id(self, request):
        operation = request.match_info['event_id']
        params = request.rel_url.query['args'].strip().split()
        return web.json_response({'result' : await self.redis.execute(operation, params)})

    async def _create_wsd_dict(self, request):
        params = self.conf._asdict()
        params['root_path_websocket'] = self._root_path_for_websocket()
        params['ws_host'] = request.host
        params['ws_scheme'] = 'wss' if request.secure else 'ws'
        params['root_path_api'] = self._root_path_for_api()
        params['api_host'] = request.host
        params['api_scheme'] = request.scheme
        params['session_id'] = await self.wss.init_session(request)
        your_wsd = namedtuple('wsd', ' '.join(self.wsd_dict.keys()))(*[v.format(**params) if type(v) is str else v for v in self.wsd_dict.values()])
        your_wsd_dict = your_wsd._asdict()
        your_wsd_dict['EVENT'] = self.context.event_handler_manager.key_ids
        return your_wsd_dict
    
class WebSocketSession():

    def __init__(self, context, sid, reconnect_timeout):
        self.context = context
        self.sid = sid
        self.context.session_store[sid] = self
        self.send_lock = asyncio.Condition()
        self.reconnect_timeout = reconnect_timeout
        self.reconnect_lock = None
        self.reconnect_until = 0
        self.request = None
        self.socket = None
        self.lock_alive_monitoring = None
        self.attrs = {}
        self.logger = logging.getLogger(__name__).getChild('ws').getChild(self.sid)

    def is_closed(self):
        return self.socket is self.reconnect_lock is None
    
    async def prepare(self, request, reconnect = False):
        reconnect_interval = max(datetime.now().timestamp() - (self.reconnect_until - self.reconnect_timeout), 0)
        self.reconnect_until = 0
        self.request = request

        if not reconnect:
            self.socket = None
            if self.reconnect_lock:
                lock = self.reconnect_lock
                self.reconnect_lock = None
                async with lock:
                    lock.notify_all()
            while self.lock_alive_monitoring:
                lock = self.lock_alive_monitoring
                try:
                    async with async_timeout.timeout(5) as cm:
                        async with lock:
                            await lock.wait()
                except asyncio.TimeoutError:
                    pass
            self.context.session_store[self.sid] = self

        self.socket = web.WebSocketResponse()
        await self.socket.prepare(self.request)
        asyncio.ensure_future(self.ping())
        
        if reconnect:
            if self.reconnect_lock:
                lock = self.reconnect_lock
                self.reconnect_lock = None
                async with lock:
                    lock.notify_all()

    async def start_alive_monitoring(self):
        self.lock_alive_monitoring = asyncio.Condition()
        
    async def end_alive_monitoring(self, closed, auth):
        if self.lock_alive_monitoring:
            lock = self.lock_alive_monitoring
            self.lock_alive_monitoring = None
            async with lock:
                lock.notify_all()
        self.context.session_store.pop(self.sid)
                
    async def closed_by_client(self):
        logger.debug("CLOSED_BY_CLIENT|SOCKET=%s|TRANSPORT=%s|IS_CLOGING=%s", self.socket.closed, self.request.transport, is_closing)

    async def start(self):
        self.logger.debug('START')
        
    async def end(self, msg):
        self.logger.debug('MSG=%s|END|TYPE=%s', id(msg), str(msg.type))

    async def send_str(self, data):
        assert self.socket is not None, 'session must be prepared to send_str'
        await self.socket.send_str(data)

    async def ping(self):
        assert self.socket is not None, 'session must be prepared to ping'
        await self.socket.ping()

    async def pong(self):
        assert self.socket is not None, 'session must be prepared to pong'
        await self.socket.pong()

    async def send_bytes_if_available(self, request_id, event_id, data, loop = False, logger = None):
        log = logger if logger else self.logger
        if self.socket is not None and not self.socket.closed:
            try:
                buf = msgpack.packb([request_id, event_id, data])
                size = len(buf)
                start = time.time()
                log.debug("SEND_BYTES|DATA=%s|MSGPACK_SIZE=%s", type(data), size)
                await asyncio.shield(self.socket.send_bytes(buf))
                log.debug("SEND_BYTES|DONE|TIME=%s, NEXT=%s", time.time()-start, loop)
                return True
            except Exception as e:
                log.exception("SEND_BYTES_ERROR=%s", e)
                
    async def send_bytes_or_wait_reconnect(self, request_id, event_id, data, loop = False, logger = None):
        log = logger if logger else self.logger
        while self.socket is not None or self.reconnect_lock is not None:
            if self.socket is not None:
                if not self.socket.closed and self.request.transport is not None:
                    is_closing = self.request.transport.is_closing()
                    start = time.time()
                    logger.debug("SEND_BYTES|TRANSPORT=%s|IS_CLOGING=%s", self.request.transport, is_closing)
                    try:
                        buf = msgpack.packb([request_id, event_id, data])
                        size = len(buf)
                        log.debug("SEND_BYTES|START|TIME=%s|DATA=%s|MSGPACK_SIZE=%s", time.time()-start, type(data), size)
                        async with self.send_lock:
                            await asyncio.shield(self.socket.send_bytes(buf))
                        log.debug("SEND_BYTES|SENTB|TIME=%s", time.time()-start)
                        await asyncio.shield(self.socket.drain())
                        log.debug("SEND_BYTES|DRAIN|TIME=%s, NEXT=%s", time.time()-start, loop)
                        return True
                    except Exception as e:
                        log.exception("SEND_BYTES_ERROR=%s", e)
                        try:
                            if self.socket is not None:
                                log.exception("SEND_BYTES_ERROR=%s", e)
                                await self.socket.close()
                        except Exception as e:
                            self.logger.exception("SOCKET_CLOSE_ERROR=%s", e)
                logger.debug("SOCKET_CLOSED|TRANSPORT=%s", self.request.transport)
                self.reconnect_lock = self.reconnect_lock if self.reconnect_lock else asyncio.Condition()
                self.reconnect_until = self.reconnect_until if self.reconnect_until > 0 else datetime.now().timestamp() + self.reconnect_timeout
                self.socket = None
            if self.reconnect_lock is not None:
                lock = self.reconnect_lock
                timeout = self.reconnect_until - datetime.now().timestamp()
                if timeout > 0:
                    try:
                        async with async_timeout.timeout(timeout) as cm:
                            async with lock:
                                await lock.wait()
                    except asyncio.TimeoutError:
                        pass
                else:
                    async with lock:
                        lock.notify_all()
                    self.reconnect_lock = None
        return False
        

class WebSocketEventSession(EventSession):

    def __init__(self, session, msg, request_id, event_id, data, received):
        super().__init__()
        self.logger = logging.getLogger(__name__).getChild('event').getChild(str(event_id)).getChild(session.sid).getChild(str(id(msg)))
        self.context = session.context
        self._redis = self.context.event_handler_manager.redis
        self._ss = session
        self._socket = session.socket
        self._msg_id = id(msg)
        self._msg_received = received
        self._request_id = request_id
        self._event_id = event_id
        self._event_data = data

    @property
    def timestamp(self):
        return self._msg_received

    #@property
    def request_id(self):
        return self._request_id

    #@property
    def session_id(self):
        return self._ss.sid

    @property
    def loop(self):
        return self.context.loop

    @property
    def redis(self):
        return self._redis

    async def get_session_attribute(self, key):
        return self._ss.attrs[key]

    async def has_session_attribute(self, key):
        return key in self._ss.attrs

    async def set_session_attribute(self, key, value):
        self._ss.attrs[key] = value

    async def get_server_attribute(self, key):
        return self.context.attrs[key]

    async def has_server_attribute(self, key):
        return key in self.context.attrs

    async def set_server_attribute(self, key, value):
        self.context.attrs[key] = value

    async def is_closed(self):
        return self._ss.is_closed()

    #need to await
    def log_message(self, request_id, event_id, data):
        return 

    async def send_bytes_if_available(self, request_id, event_id, data, loop = False):
        return await self._ss.send_bytes_if_available(request_id, event_id, data, loop, logger=self.logger)
    
    async def send_bytes_or_wait_reconnect(self, request_id, event_id, data, loop = False):
        return await self._ss.send_bytes_or_wait_reconnect(request_id, event_id, data, loop, logger=self.logger)

    async def send_str(self, data):
        await self._ss.send_str(data)

    async def ping(self):
        await self._ss.ping()

    async def pong(self):
        await self._ss.pong()

    async def closed_by_client(self):
        await self._ss.closed_by_client()

    async def start_alive_monitoring(self):
        self.logger.debug("START|ALIVE_MONITORING")
        await self._ss.start_alive_monitoring()
        
    async def end_alive_monitoring(self, closed, auth):
        self.logger.info("HANDLER_CLOSED=%s", len(closed) if closed else closed)
        try:
            await self._ss.end_alive_monitoring(closed, auth)
        finally:
            await auth.close_session(self._ss.sid)
            
        
class WebSocketServer(object):
    
    def __init__(self, context):
        self.conf = configure_module(wsserver_config)
        self.context = context
        self.auth = Auth(context)
        self.wsmsg_handler = {msg_type : lambda : self._default_wsmsg_handler
                              for msg_type in [getattr(aiohttp.WSMsgType, attr) for attr in dir(aiohttp.WSMsgType)]
                              if type(msg_type) is aiohttp.WSMsgType}
        self.wsmsg_handler[aiohttp.WSMsgType.BINARY] = lambda : self._msgpack_msg_handler
        #self.wsmsg_handler[aiohttp.WSMsgType.CONTINUATION] = lambda : self._msgpack_msg_handler
        #self.wsmsg_handler[aiohttp.WSMsgType.TEXT] = lambda : self._default_textmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.PING] = lambda : self._pingmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.PONG] = lambda : self._pongmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.CLOSE] = lambda : self._closemsg_handler

        self.event_handler = [None for v in HandleType]
        self.event_handler[HandleType.ALIVE_MONITORING.value] = self._event_handler_alive_monitoring
        self.event_handler[HandleType.ASYNC_FOR.value] = self._event_handler_async_for
        self.event_handler[HandleType.FOR.value] = self._event_handler_for
        self.event_handler[HandleType.ASYNC.value] = self._event_handler_async
        self.event_handler[HandleType.SYNC.value] = self._event_handler_sync

    async def init_session(self, request):
        return await self.auth.init_session(request)

    async def websocket_handler(self, request):
        sid, param = await self.auth.check_session(request)
        if sid in self.context.session_store:
            session = self.context.session_store[sid]
        else:
            session = WebSocketSession(self.context, sid, self.conf.reconnect_timeout)
        session.logger.info("OPEN|PARAM=%s", param)
        await session.prepare(request)
        return await self.web_socket_session_loop(session)

    async def websocket_handler_reconnect(self, request):
        sid, param = await self.auth.check_session(request)
        if sid not in self.context.session_store:
            raise web.HTTPForbidden()
        session = self.context.session_store[sid]
        session.logger.info("RECONNECT|PARAM=%s", param)
        await session.prepare(request, reconnect=True)
        return await self.web_socket_session_loop(session)

    async def web_socket_session_loop(self, session):
        await session.start()
        async for msg in session.socket:
            received = time.time()
            session.logger.debug('MSG=%s|START|TYPE=%s', id(msg), str(msg.type))
            handle = self.wsmsg_handler[msg.type]()
            try:
                assert inspect.iscoroutinefunction(handle), 'handle must be async function'
                asyncio.ensure_future(handle(session, msg, received))
            except Exception as e:
                session.logger.exception('MSG=%s|HANDLE=%s|ERROR=%s', id(msg), handle, e)
            session.logger.debug('MSG=%s|NEXT', id(msg))
            await session.end(msg)
        return session.socket

    async def _default_wsmsg_handler(self, session, msg, received):
        session.logger.debug("MSG=%s|UNHNADLED", id(msg))
        await session.send_str('N/A')
        
    async def _pingmsg_handler(self, session, msg, received):
        session.logger.debug("MSG=%s|PING", id(msg))
        await session.pong()

    async def _pongmsg_handler(self, session, msg, received):
        session.logger.debug("MSG=%s|PONG", id(msg))
        await asyncio.sleep(self.conf.ping_pong_interval)
        await session.ping()

    async def _closemsg_handler(self, session, msg, received):
        session.logger.debug("MSG=%s|CLOSE", id(msg))
        await session.closed_by_client()

    async def _msgpack_msg_handler(self, socket_session, msg, received):
        request_id, event_id, data = msgpack.unpackb(msg.data)
        event_id = int(event_id)
        session = WebSocketEventSession(socket_session, msg, request_id, event_id, data, received)
        session.logger.debug("REQUEST=%s|TYPE=%s|LEN=%s", request_id, type(data), len(data) if hasattr(data, '__len__') else 0)
        try:
            handle_type, handler = self.context.event_handler_manager.get_handler_for(event_id)
            await self.event_handler[handle_type.value](session, msg, request_id, event_id, data, handler.handle, Event(event_id, session, data))
            session.logger.debug("END".format(session.session_id(), id(msg), event_id))
        except Exception as e:
            session.logger.exception("END|ERROR=%s", e)
            if not await session.is_closed():
                event_id = -1 * event_id
                ret = '{}:{}'.format(e.__class__.__name__, e.args)
                await session.send_bytes_if_available(request_id, event_id, ret)


    async def _event_handler_alive_monitoring(self, session, msg, request_id, event_id, data, handle, event):
        await session.start_alive_monitoring()
        closed = None
        try:
            async for ret in handle(event):
                if not await session.send_bytes_or_wait_reconnect(request_id, event_id, ret, True):
                    break
            session.logger.debug("START_CLOSE_HANDLERS")
            closed = await asyncio.gather(*[f for f in [h[1].handle_closed(session) for h in session.context.event_handler_manager.handlers()] if inspect.isawaitable(f)])
        finally:
            await session.end_alive_monitoring(closed, self.auth)
    
    async def _event_handler_async_for(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|AWAIT_ASYNC_LOOP")
        async for ret in handle(event):
            if not await session.send_bytes_or_wait_reconnect(request_id, event_id, ret, True):
                return False
        return True

    async def _event_handler_for(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|SYNC_LOOP")
        for ret in handle(event):
            if not await session.send_bytes_or_wait_reconnect(request_id, event_id, ret, True):
                return False
        return True

    async def _event_handler_async(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|AWAIT_ASYNC_HANDLE")
        ret = await handle(event)
        return await session.send_bytes_or_wait_reconnect(request_id, event_id, ret)

    async def _event_handler_sync(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|SYNC_HANDLE")
        ret = handle(event)
        return await session.send_bytes_or_wait_reconnect(request_id, event_id, ret)

        
