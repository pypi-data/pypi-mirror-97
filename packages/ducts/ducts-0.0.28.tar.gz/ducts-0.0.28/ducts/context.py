import os
import sys
from pathlib import Path
import importlib
from importlib import machinery
import inspect

import concurrent

import logging

from .redis import RedisClient
from .common import get_conf
from .event import HandlerManager

from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr_list('plugin_modules', [], help='module names for plugin base directory')
    loader.add_attr_int('max_workers', 1, help='max threadpool workers')

class ServerContext:

    def __init__(self, loop):
        self.logger = logging.getLogger(__name__).getChild('manager')
        self.conf = configure_module(config, override=get_conf())
        self.loop = loop
        self.session_store = {}
        self.redis = RedisClient(self.loop)
        self.event_handler_manager = HandlerManager(self)
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.conf.max_workers)
        self.attrs = {}

    async def setup(self):
        await self.redis.connect()
        await self.event_handler_manager.setup()

    async def run(self):
        await self.event_handler_manager.run()

    def module_path(self, path):
        return path.resolve() if path.is_absolute() else Path(__file__).parent.joinpath(path).resolve()

    def resolve_local_path(self, path):
        return path.resolve() if path.is_absolute() else self.conf.ducts_home.joinpath(path).resolve()

    def plugin_paths(self, module_path, local_path):
        yield (Path(__file__).parent.joinpath(module_path), 0)
        for module_name in self.conf.plugin_modules:
            yield (Path(importlib.import_module(module_name).__file__).parent.joinpath(module_path), 1)
        yield (self.resolve_local_path(local_path), 2)

    async def run_in_executor(self, func):
        return await self.loop.run_in_executor(self.thread_pool, func)

    async def close(self):
        await self.redis.close()

    
