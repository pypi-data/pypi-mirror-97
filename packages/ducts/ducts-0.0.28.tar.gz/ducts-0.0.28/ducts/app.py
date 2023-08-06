#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from importlib import import_module
import psutil
from pathlib import Path
import functools
import traceback
import argparse

from daemon import DaemonContext
from daemon.pidfile import TimeoutPIDLockFile

from ifconf import configure_module, config_callback, configure_main

@config_callback
def config(loader):
    loader.add_attr('module', 'ducts.main', help='module_name containing the main module to run command')
    loader.add_attr('service', 'run', help='method_name to run service process')


def start(pidfile, run):
    if pidfile.is_locked():
        raise Exception('Process is already started.')
    current_dir = os.getcwd()
    with DaemonContext(
            pidfile=pidfile
            , stdout = sys.stdout
            , stderr = sys.stderr):
        os.chdir(current_dir)
        run()
    
def stop(pidfile, run):
    if not pidfile.is_locked():
        return
    pid = pidfile.read_pid()
    for i in range(5):
        try:
            p = psutil.Process(pid)
            print('Terminating PID={}...'.format(pid))
            p.terminate()  #or p.kill()
            p.wait(timeout=3)
        except psutil.TimeoutExpired:
            continue
        except psutil.NoSuchProcess:
            break
    for i in range(3):
        try:
            p = psutil.Process(pid)
            print('Killing PID={}...'.format(pid))
            p.kill()
            p.wait(timeout=1)
        except psutil.TimeoutExpired:
            continue
        except psutil.NoSuchProcess:
            break

        
def main(parser = None, config_arg = 'config_{module}.ini', callback_methods = []):
    parser = parser if parser else argparse.ArgumentParser()
    parser.add_argument('module', help='module_name to run command.')
    parser.add_argument('command', help='[start|stop]')
    main_config = configure_main(argparser = parser, config_arg = config_arg, callback_methods = callback_methods)
    module_config = configure_module(config)
    
    run = getattr(import_module('{}.{}'.format(module_config.module, main_config.args.module)), module_config.service)
    command = getattr(import_module(main.__module__), main_config.args.command)
    
    import ducts.common as c
    pidfile = TimeoutPIDLockFile(c.get_pidfile(main_config.args.module, module_config.service))

    command(pidfile, run)
    
    
