#!/usr/bin/env python3

import sys
import traceback
import logging

import asyncio

from ifconf import configure_module, config_callback, configure_main

from ducts.backend.asr import AutomaticSpeechRecognizerManager

def run():
    logger = logging.getLogger(__name__)
    loop = asyncio.get_event_loop()
    asr = AutomaticSpeechRecognizerManager(loop)
    asyncio.ensure_future(asr.run())
    try:
        loop.run_forever()
    except Exception as e:
        logger.exception('Error on loop: %s', e)
    except BaseException as e:
        logger.info(e)
    try:
        logger.info('Closing...')
        loop.run_until_complete(asr.close())
    except Exception as e:
        logger.exception('Error on close: %s', e)
    except BaseException as e:
        logger.info(e)

    try:
        logger.info('Shutdown...')
        loop.run_until_complete(loop.shutdown_asyncgens())
    except Exception as e:
        logger.exception('Error on shutdown: %s', e)
    except BaseException as e:
        logger.info(e)
    finally:
        loop.close()
        logger.info('Completed. See you!')

def main():
    configure_main()
    run()
    
if __name__ == '__main__':
    main()
