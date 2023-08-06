#!/usr/bin/env python3
# coding: utf-8

import sys

from .app import main
    
if __name__ == '__main__':
    import ducts.server
    import ducts.redis

    callback_methods = [ducts.common.config, ducts.redis.config, ducts.server.config, ducts.server.wsserver_config]
    if len(sys.argv) > 1:
        if sys.argv[1] == 'asr':
            import ducts.backend.asr
            callback_methods = [ducts.common.config, ducts.redis.config, ducts.backend.asr.config]

    main(config_arg = 'config_{module}.ini', callback_methods = callback_methods)
    
