# _*_ coding:utf-8 _*_

import os
from collector.utils import config

# 初始化目录
if not os.path.exists(config.CACHE_DIR):
    os.makedirs(config.CACHE_DIR)
