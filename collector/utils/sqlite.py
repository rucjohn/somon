# _*_ coding:utf-8 _*_

import os
import sqlite3
from collector.utils import config

database = os.path.join(config.CACHE_DIR, config.DB_NAME)


class SQLiteConnection(object):

    def __init__(self, name=database):
        self.name = name
        self.conn = None
        self.cursor = None
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor and self.conn:
            self.cursor.close()
            self.conn.close()

    def execute_one(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row

    def execute_all(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        rows = self.cursor.fetchall()
        return rows
