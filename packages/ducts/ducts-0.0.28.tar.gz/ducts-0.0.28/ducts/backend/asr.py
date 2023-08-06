#!/usr/bin/env python3

import sys
import os.path

import traceback


import threading
from concurrent.futures import ThreadPoolExecutor
#from concurrent.futures import ProcessPoolExecutor

import functools
#from queue import Queue, Empty
from io import BytesIO
import time
from datetime import datetime

import asyncio
import aiofiles

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

from ifconf import configure_module, config_callback, configure_main

from ducts.redis import RedisClient

import logging

        
@config_callback()
def config(loader):
    loader.add_attr('key', 'ASR/QUEUE', hidden=True, help='list key for asr')
    loader.add_attr_int('timeout_list_for_asr', 10, hidden=True, help='timeout for asr waiting in sec. can be 0.')
    loader.add_attr_int('timeout_stream_read', 2000, hidden=True, help='timeout for stream read in msec. cannot be 0.')
    loader.add_attr_int('timeout_thread_asr_lock', 10, hidden=True, help='timeout for asr waiting in sec. can be 0.')
    loader.add_attr('asr_language_code', 'ja-JP', help='')
    loader.add_attr_int('asr_sample_rate_hertz', 16000, help='')
    loader.add_attr_boolean('debug_store_pcm_enabled', False, help='')
    loader.add_attr('debug_store_pcm_fmt', './{}.{}.{}', help='')
    loader.add_attr_float('timeout_no_response', 0.5, hidden=True, help='timeout for wait response in sec. if 0, no timeout.')
    

class AutomaticSpeechRecognizerManager(object):

    def __init__(self, loop):
        self.conf = configure_module(config)
        self.loop = loop
        self.redis = RedisClient(loop)
        self.thread_pool = ThreadPoolExecutor(max_workers=256)
        self.speech_client = speech.SpeechClient()
        
        self.audio_stream_key_dict = {}
        self.audio_input_lock = asyncio.Condition()
        
    async def run(self):
        await self.redis.connect()
        self.reids_connection = await self.redis.connect_for_blocking(2, 8)
        asyncio.ensure_future(self.listen_list_for_asr())
        asyncio.ensure_future(self.listen_audio_input())

    async def listen_list_for_asr(self):
        logger = logging.getLogger(__name__).getChild('manager').getChild('listen_list')
        listkey = self.conf.key
        logger.info('START|KEY=%s', listkey)
        with await self.reids_connection as conn:
            while True:
                try:
                    logger.debug('BLOCK|TIMEOUT=%s', self.conf.timeout_list_for_asr)
                    spec_key = await conn.execute('BLPOP', listkey, self.conf.timeout_list_for_asr, encoding=None)
                    if spec_key:
                        logger.info('POP|SPEC_KEY=%s', spec_key[1])
                        spec = await self.redis.xlast_str(spec_key[1])
                        logger.debug('POP|SPEC=%s', spec)
                        if not spec:
                            logger.warn('INVALID_SPEC_KEY|EMPTY|SPEC_KEY=%s', spec_key[1])
                            continue
                        handler = AutomaticSpeechRecognizerThread(spec, self)
                        ret = await self.redis.execute('XREVRANGE', handler.stream_key, '+', '-', 'COUNT', 1)
                        handler.stream_id = ret[0][0] if ret else handler.stream_id
                        handler.future = self.loop.run_in_executor(self.thread_pool, handler.run)
                        asyncio.ensure_future(handler.future)
                        self.audio_stream_key_dict[handler.stream_key] = handler
                        if len(self.audio_stream_key_dict) == 1:
                            async with self.audio_input_lock:
                                self.audio_input_lock.notify_all()
                except Exception as e:
                    logger.exception('ERROR=%s', e)
        logger.info('END|KEY=%s', listkey)
        
            
    async def listen_audio_input(self):
        logger = logging.getLogger(__name__).getChild('manager').getChild('listen_audio')
        logger.info('START')
        with await self.reids_connection as conn:
            while True:
                try:
                    while not self.audio_stream_key_dict:
                        logger.debug('LOCK_WAIT')
                        async with self.audio_input_lock:
                            await self.audio_input_lock.wait()
                        logger.debug('LOCK_NOTIFIED|KEYS=%s', self.audio_stream_key_dict)
                    keys = list(self.audio_stream_key_dict.keys())
                    values = [h.stream_id for h in self.audio_stream_key_dict.values()]
                    logger.debug('BLOCK|STREAM=%s|TIMEOUT=%s', self.audio_stream_key_dict.items(), self.conf.timeout_stream_read)
                    ret = await conn.execute('XREAD', 'COUNT', 10, 'BLOCK', self.conf.timeout_stream_read, 'STREAMS', *keys, *values, encoding=None)
                    if not ret:
                        for del_key in [k for k,v in self.audio_stream_key_dict.items() if v.flg_exit]:
                            self.audio_stream_key_dict.pop(del_key)
                        continue
                    for stream_result in ret:
                        stream_key = stream_result[0].decode('UTF-8')
                        logger.debug('XREAD|STREAM=%s', stream_key)
                        handler = self.audio_stream_key_dict[stream_key]
                        for result in stream_result[1]:
                            id = result[0]
                            value = {v[0].decode('UTF-8') : v[1] for v in zip(*[iter(result[1])]*2)} 
                            handler.append(id, value)
                except Exception as e:
                    logger.exception('ERROR|TYPE=%s', e)
                    await asyncio.sleep(1)
        logger.info('END')

    async def close(self):
        await self.redis.close()

file_index = 0
def next_index():
    global file_index
    file_index += 1
    return file_index
    
class AutomaticSpeechRecognizerThread(object):

    def __init__(self, spec, manager):
        for key,value in spec.items():
            setattr(self, key, value)
        self.stream_key = self.AUDIO_STREAM_KEY
        self.asr_pubsub_key = self.ASR_PUBSUB_KEY
        self.asr_stream_key = self.ASR_STREAM_KEY
        self.result_pubsub_key = self.RESULT_PUBSUB_KEY
        self.result_stream_key = self.RESULT_STREAM_KEY
        
        self.manager = manager
        self.conf = manager.conf
        self.speech_client = manager.speech_client
        self.stream_id = '0'
        self.future = None
        
        self.queue = []
        self.lock = threading.Condition()
        self.time_last_response = 0
        self.flg_exit = False
        
        self.filename = self.stream_key.split('/')[0].replace(':','.')


    def generator(self):
        self.path_index = next_index()
        thread_id = threading.get_ident()
        logger = logging.getLogger(__name__).getChild('generator').getChild(str(thread_id))
        logger.info('START|KEY=%s', self.stream_key)
        if self.conf.debug_store_pcm_enabled:
            with open(self.conf.debug_store_pcm_fmt.format(self.filename, self.path_index, 'pcm'), 'wb') as f:
                pass
        while not self.flg_exit:
            try:
                logger.debug('LOCK|QUEUE=%s', len(self.queue))
                with self.lock:
                    loop_count = 0
                    while len(self.queue) == 0:
                        if not self.lock.wait(5):
                            logger.debug('WAIT_TIMEOUT|LOOP_COUNT=%s|FLG_EXIT=%s', loop_count, self.flg_exit)
                            loop_count += 1
                            if self.flg_exit:
                                raise GeneratorExit()
                    if None in self.queue:
                        self.flg_exit = True
                        raise GeneratorExit()
                    data = b''.join(self.queue)
                    self.queue.clear()
                logger.debug('NOTIFIED|DATA=%s', len(data))
                if self.conf.debug_store_pcm_enabled:
                    with open(self.conf.debug_store_pcm_fmt.format(self.filename, self.path_index, 'pcm'), 'ab') as f:
                        f.write(data)
                yield data
                waiting = time.time() - self.time_last_response if self.time_last_response > 0 else 0
                if waiting > self.conf.timeout_no_response and self.conf.timeout_no_response > 0:
                    self.time_last_response = 0
                    logger.debug('NO_RESPONSE|WAIT=%s', waiting)
                    break
            except GeneratorExit as e:
                logger.warn('GENERATOR_EXIT')
                #raise e
                break
            except Exception as e:
                logger.exception('ERROR=%s', e)
                break
        logger.info('EXIT')

    def run(self):
        thread_id = threading.get_ident()
        logger = logging.getLogger(__name__).getChild('asr_thread').getChild(str(thread_id))
        logger.info('RUN|KEY=%s', self.stream_key)
        try:
            #loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(loop)

            pubkey = self.asr_pubsub_key + str(datetime.now().timestamp())
            streamkey = self.asr_stream_key
            self.manager.redis.execute_threadsafe(
                self.manager.redis.xadd_and_publish
                , pubkey
                , streamkey
                , STATE = 'RUNNING'
                , REQUEST_ID='ASR'
                , THREAD = thread_id)
            
            with self.lock:
                while len(self.queue) == 0:
                    logger.debug('START_LOCK|QUEUE=%s|TIMEOUT=%s', len(self.queue), self.conf.timeout_thread_asr_lock)
                    ret = self.lock.wait(self.conf.timeout_thread_asr_lock)
            logger.debug('START_LOCK_END|QUEUE=%s', len(self.queue))
                        
            config = types.RecognitionConfig(
                encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
                , sample_rate_hertz = self.manager.conf.asr_sample_rate_hertz
                , language_code = self.manager.conf.asr_language_code
            )
            streaming_config = types.StreamingRecognitionConfig(
                config = config
                , interim_results = True
                , single_utterance = False
            )
            while not self.flg_exit:
                self.time_last_response = 0
                logger.info('START|KEY=%s', self.stream_key)

                #https://github.com/googleapis/google-cloud-python/issues/6077
                #client = speech.SpeechClient()
                requests = (types.StreamingRecognizeRequest(audio_content=content) for content in self.generator())

                logger.debug('1.STREAM_RECOGNIZE|CONFIG=%s', streaming_config)
                responses = self.speech_client.streaming_recognize(streaming_config, requests)
                logger.debug('2.GOT_RESPONSES=%s', responses)

                for count, response in enumerate(responses):
                    self.time_last_response = time.time()
                    logger.debug('3.1.RESPONSE|%s=%s', count, response)
                    #if utterance != "" and time.time() - prev_get_time >= 0.5: # 最後に発話を取得してから0.5秒後に送信
                    #raise Exception
                    #    break
                    if not (response.results and response.results[0].alternatives):
                        logger.debug('3.x.RESPONSE_WITH_NO_RESULT')
                        continue
                    result = response.results[0]
                    utterance = result.alternatives[0].transcript
                    is_final = result.is_final
                    prob = result.alternatives[0].confidence if is_final else result.stability
                    result_end_time = result.result_end_time.seconds + result.result_end_time.nanos / 1000000000
                    logger.debug('3.2.RESULT%s(%s,%s)|%s', count, is_final, prob, utterance)

                    pubkey = self.result_pubsub_key + str(datetime.now().timestamp())
                    streamkey = self.result_stream_key
                    self.manager.redis.execute_threadsafe(
                        self.manager.redis.xadd_and_publish
                        , pubkey
                        , streamkey
                        , BEHAVIOR=utterance
                        , REQUEST_ID='ASR'
                        , IS_FINAL=1 if is_final else 0
                        , PROB=prob
                        , RESULT_END_TIME=result_end_time)
                    if is_final:
                        break
        except Exception as e:
            logger.exception('ERROR=%s', e)
            state = 'ERROR'
            error = traceback.format_exc()
        else:
            state = 'END'
            error = ''

        pubkey = self.asr_pubsub_key + str(datetime.now().timestamp())
        streamkey = self.asr_stream_key
        self.manager.redis.execute_threadsafe(
            self.manager.redis.xadd_and_publish
            , pubkey
            , streamkey
            , STATE = state
            , TRACEBACK = error
            , REQUEST_ID='ASR'
            , THREAD = thread_id)
        self.flg_exit = True
        logger.info('EXIT')
                
    def append(self, id, value):
        self.stream_id = id
        with self.lock:
            self.queue.append(value.get('AUDIO', None))
            self.lock.notify_all()
        
        
