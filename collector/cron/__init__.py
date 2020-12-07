# _*_ coding:utf-8 _*_

import os
from collector.utils import config, sqlite

init_sql = '''
           CREATE TABLE JOB(
             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             name VARCHAR(30) NOT NULL,
             timer VARCHAR(100) NOT NULL,
             module VARCHAR(100) NOT NULL,
             create_time TIMESTAMP default (datetime('now', 'localtime'))
           );
           '''

tasks = [
    dict(name='application', timer='*/30 * * * *', module='collector.cron.task.application'),
    dict(name='process', timer='* * * * *', module='collector.cron.task.process'),
    dict(name='screen', timer='* * * * *', module='collector.cron.task.screen')
]

database = config.DB_NAME
if not os.path.exists(database):
    client = sqlite.SQLiteConnection(name=database)
    client.execute_all(sql=init_sql)
    for task in tasks:
        task_name, task_timer, task_module = task['name'], task['timer'], task['module']
        sql = '''INSERT INTO JOB(name, timer, module) VALUES ('{0}', '{1}', '{2}')'''.format(
            task_name, task_timer, task_module
        )
        client.execute_all(sql=sql)
