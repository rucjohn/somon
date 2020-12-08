# _*_ coding:utf-8 _*_

import os
import time
from collector.cron import schedules
from collector.utils import sqlite, config
from collector.cron.actions import application

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
        task = 'application'
        if is_valid(task):
            result = application.responses()
            print(result)
        time.sleep(wait)


if __name__ == '__main__':
    ret = is_valid(task='application')
    print(ret)

