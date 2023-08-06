import base64
import binascii

from aiohttp import hdrs, web
from datetime import datetime

import inspect
import hashlib
import base64

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)
        
@config_callback
def config(loader):
    loader.add_attr('hash_algorithm', 'sha1', help='hash algorithm name for session')
    loader.add_attr_list('white_paths', ['/libs/', '/wsd', '/main'], help='paths without authentication')
    loader.add_attr('stream_key_for_session_opened', 'SESSION/2020', help='stream key for session')
    loader.add_attr('stream_key_for_session_closed', 'SESSION/CLOSED', help='stream key for session')


class Auth(object):


    def __init__(self, context):
        self.conf = configure_module(config)
        self.context = context
        for k,v in inspect.getmembers(hashlib, inspect.isbuiltin):
            if k == self.conf.hash_algorithm:
                self.hash_func = v
                break
        if not hasattr(self, 'hash_func'):
            raise ValueError('hash algorithm[{}] not found.'.format(self.conf.hash_algorithm_key))

    async def init_session(self, request):
        ip, port = request.transport.get_extra_info('peername')
        ua = request.headers.get('User-Agent', '')
        query = request.rel_url.query
        key = query.get('uuid', None)
        key = key if key else query.get('ts', None)
        if not key:
            raise web.HTTPForbidden()
        ssid = self.hash_func(ip.encode()+str(port).encode()+ua.encode()+key.encode()).hexdigest()
        tsid = await self.context.redis.xadd(self.conf.stream_key_for_session_opened, ip=ip, port=port, ua=ua, ssid=ssid, **query)
        return "{}.{}".format(ssid, base64.b64encode(tsid).decode())

    async def check_session(self, request):
        ssid, tsids = request.match_info['session_id'].split('.')
        tsid = base64.b64decode(tsids).decode()
        ts = datetime.fromtimestamp(int(tsid.split('-')[0])/1000)
        ip, port = request.transport.get_extra_info('peername')
        ua = request.headers.get('User-Agent', '')
        param = await self.context.redis.xget_str(self.conf.stream_key_for_session_opened, tsid)
        if param['ssid'] != ssid: #or param['ua'] != ua:
            raise web.HTTPForbidden()
        return 'SS.'+tsids, param
    
        #op = int(param['port'])
        #if param['ip'] != ip or port > op+128 or (op > 65535 - 128 and port > 49152 + 128):
        #    raise web.HTTPForbidden()

    async def close_session(self, session_id):
        tsid = base64.b64decode(session_id[len('SS.'):].encode())
        param = await self.context.redis.xget_str(self.conf.stream_key_for_session_opened, tsid)
        if param:
            await self.context.redis.xadd(self.conf.stream_key_for_session_closed, tsid=tsid, **param)

    async def setup(self, app):
        app.middlewares.append(self.middleware)

    async def raise_error(self, request):
        raise web.HTTPUnauthorized(
            headers={
                hdrs.WWW_AUTHENTICATE: 'Basic realm={}'.format(self._realm)
            },
        )

    @web.middleware
    async def middleware(self, request, handler):
        if request.path not in self._white_paths:
            auth_header = request.headers.get(hdrs.AUTHORIZATION)

            if auth_header is None or not auth_header.startswith('Basic '):
                return await self.raise_error(request)

            try:
                secret = auth_header[6:].encode('utf-8')

                auth_decoded = base64.decodebytes(secret).decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError,
                    binascii.Error):
                await self.raise_error(request)

            credentials = auth_decoded.split(':')

            if len(credentials) != 2:
                await self.raise_error(request)

            username, password = credentials

            if username != self._username or password != self._password:
                await self.raise_error(request)

        return await handler(request)
