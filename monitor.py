# _*_ coding:utf-8 _*_

import os
import sys
import time
import random
import threading

from collector.cron import tasks
from collector.listener import keyboard, mouse


class Collect(object):

    def __init__(self):
        self.threads = dict()

    def add(self, func, name, *args, **kwargs):
        thread = threading.Thread(target=func, name=name, args=args, kwargs=kwargs)
        self.threads.update({name: thread})
        # self.threads.append((name, thread))

    def start(self):
        for name, thread in self.threads.items():
            # 随机休眠，避免同一时间触发所有任务
            _ = random.randint(5, 15)
            print("{0} 随机休眠: {1}".format(name, _))
            time.sleep(_)
            thread.start()

    def wait(self):
        for _, thread in self.threads.items():
            thread.join()


def collect():
    app = Collect()
    # 添加监听器
    app.add(keyboard.run, 'Listener_keyboard')
    app.add(mouse.run, 'Listener_mouse')
    # 添加定时任务
    app.add(tasks.exec_application, 'Cron_application')
    app.add(tasks.exec_process, 'Cron_process')
    app.add(tasks.exec_screen, 'Cron_screen')
    app.add(tasks.exec_count_km, 'Cron_count_keyboardmouse')
    # app.add(cache.run, 'Listener-cache')
    # 启动
    app.start()
    app.wait()


if __name__ == '__main__':
    collect()
