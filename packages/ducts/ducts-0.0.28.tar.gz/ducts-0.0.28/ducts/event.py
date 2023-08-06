import os
import sys
from pathlib import Path
import importlib
from importlib import machinery
import abc
import inspect

from collections import namedtuple
from collections import OrderedDict
from enum import Enum

from ifconf import configure_module, config_callback

import asyncio

import logging

from .spi import HandlerSpec, EventHandler, EventHandlerManager

@config_callback
def config(loader):
    loader.add_attr_path('module_path_handler', Path('./handler'), help='module path for event_handler files')
    loader.add_attr_path('local_path_handler', Path('./handler'), help='local path for event_handler files')
    loader.add_attr('plugin_filename_pattern', 'evt_*.py', help='event handler plugin filename pattern')
    loader.add_attr_int('min_user_handler_id', 1000, help='minimum handler ID for user plugin')

    
class HandleType(Enum):
    ALIVE_MONITORING = 0
    ASYNC_FOR = 1
    FOR = 2
    ASYNC = 3
    SYNC = 4

    
class HandlerManager(EventHandlerManager):

    def __init__(self, context):
        self.logger = logging.getLogger(__name__).getChild('manager')
        self.conf = configure_module(config)
        self.context = context
        self.loop = context.loop
        self._redis = context.redis
        self._helpers = {}
        self.specs = []
        self.key_ids = {}
        self._handlers = OrderedDict()
        self._plugin_dirs = []

    @property
    def redis(self):
        return self._redis

    async def setup(self):
        for path, level in self.context.plugin_paths(self.conf.module_path_handler, self.conf.local_path_handler):
            await self.load_plugins(path, level < 2)

    async def run(self):
        for t,h in self._handlers.values():
            f = asyncio.ensure_future(h.run(self))
            f.add_done_callback(self.done_callback)

    def done_callback(self, future):
        pass

    async def load_plugins(self, plugin_dir, is_system_handler):
        if is_system_handler:
            self.logger.debug('SYSTEM_PLUGIN_DIR=%s', plugin_dir)
        else:
            self.logger.info('PLUGIN_DIR=%s', plugin_dir)
        self._plugin_dirs.insert(0, plugin_dir)
        local_modules = set()
        for p in plugin_dir.glob(self.conf.plugin_filename_pattern):
            loader = machinery.SourceFileLoader(p.stem, str(p))
            module = loader.load_module()
            local_modules.add(module.__name__)
        for cls in sorted(EventHandler.__subclasses__(), key=lambda x: (str(x), x)):
            h = cls()
            if h.__class__.__module__ not in local_modules:
                continue
            spec = await self.setup_handler(h, is_system_handler)
            if spec is None:
                continue
            self.specs.append(spec)
            self.key_ids[spec.key] = spec.id if not spec.key in self.key_ids else max(self.key_ids[spec.key], spec.id)
            if spec.id == 0:
                htype = HandleType.ALIVE_MONITORING
            elif inspect.isasyncgenfunction(h.handle):
                htype = HandleType.ASYNC_FOR
            elif inspect.isgeneratorfunction(h.handle):
                htype = HandleType.FOR 
            elif inspect.iscoroutinefunction(h.handle):
                htype = HandleType.ASYNC
            else:
                htype = HandleType.SYNC
            self._handlers[spec.id] = (htype, h)
        if self.logger.isEnabledFor(logging.DEBUG):
            for s in self.specs:
                self.logger.debug('HANDLER|SPEC=%s', s)
        

    async def setup_handler(self, handler, is_system_handler):
        index = 0
        for ids in handler.__module__.split('_'):
            try:
                index += (len(ids) + 1)
                id = int(ids)
                setattr(handler, 'ID', id)
                key = getattr(handler, handler.ATTR_KEY, handler.__module__[index:])
                if not key:
                    key = 'undefined'
                key = key.upper()
                setattr(handler, handler.ATTR_KEY, key)
                callback = inspect.isasyncgenfunction(handler.handle) or inspect.isgeneratorfunction(handler.handle)
                #desc = handler.description()
                if id < self.conf.min_user_handler_id and not is_system_handler:
                    self.logger.warn('Permission denied. User handler ID must be less than [%s] but was [%s]', self.conf.min_user_handler_id, id)
                    return None
                spec = HandlerSpec(id, key, callback)
                ret = handler.setup(spec, self)
                return ret if not inspect.isawaitable(ret) else await ret
            except ValueError:
                continue

    def load_helper_module(self, module_name):
        return self._helpers[module_name] if module_name in self._helpers else self._new_helper_module(module_name)

    def get_handler_for(self, event_id):
        return self._handlers[event_id]

    def handlers(self):
        return self._handlers.values()

    def _new_helper_module(self, module_name):
        for plugin_dir in self._plugin_dirs:
            p = plugin_dir.joinpath("{}.py".format(module_name))
            loader = machinery.SourceFileLoader(module_name, str(p))
            module = loader.load_module()
            self._helpers[module_name] = module
            return module
        
    async def get_server_attribute(self, key):
        return self.context.attrs[key]

    async def has_server_attribute(self, key):
        return key in self.context.attrs

    async def set_server_attribute(self, key, value):
        self.context.attrs[key] = value

    


