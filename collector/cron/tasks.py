# _*_ coding:utf-8 _*_

import os
import time
from collector.cron import schedules
from collector.utils import sqlite
from collector.cron.actions import application, process, screen, keyboardmouse

wait = 60


def is_valid(task):
    client = sqlite.SQLiteConnection()
    row = client.execute_one('''SELECT * from JOB WHERE name="{0}"'''.format(task))
    if not row:
        return False
    timer = schedules.transform_cron_timer(row[2])
    if schedules.Cron(**timer).is_valid():
        return True
    else:
        return False


def exec_application():
    while True:
        task = application.__TASK__
        if is_valid(task):
            result = application.responses()
            print(result)
        time.sleep(wait)


def exec_process():
    while True:
        task = process.__TASK__
        if is_valid(task):
            result = process.response()
            print(result)
        time.sleep(wait)


def exec_screen():
    while True:
        task = screen.__TASK__
        if is_valid(task):
            result = screen.capture()
            print(result)
        time.sleep(wait)


def exec_count_km():
    while True:
        task = keyboardmouse.__TASK__
        if is_valid(task):
            result = keyboardmouse.response()
            print(result)
        time.sleep(wait)


if __name__ == '__main__':
    ret = is_valid(task='process')
    print(ret)

