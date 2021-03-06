# _*_ coding:utf-8 _*_

import os
from collector.utils import sqlite

init_sql = '''
           CREATE TABLE JOB(
             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             name VARCHAR(30) NOT NULL,
             timer VARCHAR(100) NOT NULL,
             module VARCHAR(100) NOT NULL,
             create_time TIMESTAMP default (datetime('now', 'localtime'))
           );
           '''

lists = [
    dict(name='APPLICATION', timer='* * * * *', module='collector.cron.actions.application'),
    dict(name='PROCESS', timer='* * * * *', module='collector.cron.actions.process'),
    dict(name='SCREEN', timer='* * * * *', module='collector.cron.actions.screen'),
    dict(name='KM', timer='* * * * *', module='collector.cron.actions.keyboardmouse')
]

database = sqlite.database
if not os.path.exists(database):
    client = sqlite.SQLiteConnection(database)
    client.execute_all(sql=init_sql)
    for task in lists:
        task_name, task_timer, task_module = task['name'], task['timer'], task['module']
        sql = '''INSERT INTO JOB(name, timer, module) VALUES ('{0}', '{1}', '{2}')'''.format(
            task_name, task_timer, task_module
        )
        client.execute_all(sql=sql)
