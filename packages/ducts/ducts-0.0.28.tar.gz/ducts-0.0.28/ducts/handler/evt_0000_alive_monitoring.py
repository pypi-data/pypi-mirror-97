from ducts.spi import EventHandler

import time

import asyncio

from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr_int('alive_monitoring_interval', 20, help='Ping interval from the server [sec]')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('死活監視用メインループを開始します。最初に一度だけ自動的に呼び出されます。サーバ時刻を定期的に返します。')
        return handler_spec

    async def handle(self, event):
        yield (time.time(), event.session.timestamp)
        while not await event.session.is_closed():
            await asyncio.sleep(self.conf.alive_monitoring_interval)
            yield (time.time(), event.session.timestamp)
        
    


