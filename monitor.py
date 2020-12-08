# _*_ coding:utf-8 _*_

import os
import sys
import time
import random
import platform
import logging
import subprocess
import threading

from collector.cron import crond
from collector.cron import tasks
# from collector.listener import cache, keyboard, mouse


class Collect(object):

    def __init__(self):
        self.threads = []

    def add(self, func, name, *args, **kwargs):
        thread = threading.Thread(target=func, name=name, args=args, kwargs=kwargs)
        self.threads.append(thread)

    def start(self):
        for thread in self.threads:
            # 随机休眠，避免同一时间触发所有任务
            _ = random.randint(1, 30)
            print("随机休眠: {}".format(_))
            time.sleep(_)
            thread.start()

    def wait(self):
        for thread in self.threads:
            thread.join()


def collect():
    app = Collect()
    # 添加定时任务
    app.add(tasks.exec_application, 'Cron')
    # # 添加缓存监听器
    # app.add(cache.run, 'Listener-cache')
    # # 添加键盘监听器
    # app.add(keyboard.run, 'Listener-keyboard')
    # # 添加鼠标监听器
    # app.add(mouse.run, 'Listener-mouse')
    # 启动
    app.start()
    app.wait()


# def collectA():
#     logging.info(u"启动scheduler: Collect")
#     basedir = os.path.dirname(os.path.abspath(__file__))
#     collect_dir = os.path.join(basedir, 'collect')
#     try:
#         os.chdir(collect_dir)
#     except OSError:
#         return False
#     if not os.path.exists('main.py'):
#         logging.info(u"调用主进程失败")
#         return False
#     logging.info(u"调用主进程")
#     cmd = r'c:\salt\bin\python.exe main.py {0}'.format(task)
#     subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     return True
#
#
# def t_collect():
#     return "collect task"


if __name__ == '__main__':
    collect()
