# _*_ coding:utf-8 _*_

import os

from pynput import mouse
from collector.utils import common

__TASK__ = 'MOUSE'
cache_dir = common.get_cache_dir(sub_name=__TASK__)


def on_click(x, y, button, pressed):
    try:
        if pressed:
            _, dt_str = common.get_time_info(fmt="%Y-%m-%d-%H-%M")
            save_path = os.path.join(cache_dir, dt_str)
            with open(save_path, 'a') as fd:
                fd.write(str(1) + '\n')
    except AttributeError:
        pass


def on_release(key):
    print('released key: {0}'.format(key))


def run():
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.join()


if __name__ == '__main__':
    run()
