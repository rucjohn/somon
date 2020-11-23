# _*_ coding:utf-8 _*_

from __future__ import absolute_import, unicode_literals
import os
import configparser


path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'config',
    'config.ini'
)

cf = configparser.ConfigParser()
cf.read(path)

# cache
CACHE_DIR = cf.get('cache', 'cache_dir')
