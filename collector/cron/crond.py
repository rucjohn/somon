# _*_ coding:utf-8 _*_

import sys
import threading
import traceback
from . import schedules
from collector.utils import sqlite


class MyThread(object):

    def __init__(self):
        self.threads = []

    def add(self, func, name, *args, **kwargs):
        thread = threading.Thread(target=func, name=name, args=args, kwargs=kwargs)
        self.threads.append(thread)

    def start(self):
        for thread in self.threads:
            thread.start()

    def wait(self):
        for thread in self.threads:
            thread.join()


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class {} cannot be found ({})'.format(
            class_str, traceback.format_exception(*sys.exc_info())
        ))


def run():

    my_thread = MyThread()

    client = sqlite.SQLiteConnection()
    rows = client.execute_all('''SELECT * from JOB''')
    for row in rows:
        task_name = row[1]
        task_timer = schedules.transform_cron_timer(row[2])
        task_module = row[3]
        if not task_module:
            continue
        if schedules.Cron(**task_timer).is_valid():
            my_thread.add(import_class(task_module), task_name)

    my_thread.start()
    my_thread.wait()


