# _*_ coding:utf-8 _*_

import os
import json
import time
import datetime
import hashlib
from collector.utils import config


def ordered_dict():
    try:
        import collections
        cls = collections.OrderedDict()
    except (ImportError, AttributeError):
        cls = dict()
    return cls


def timestamp():
    return int(time.time())


def gen_code(data):
    md5 = hashlib.md5()
    try:
        if isinstance(data, list):
            data.sort()
            md5.update(json.dumps(data))
        elif isinstance(data, dict):
            md5.update(json.dumps(data, sort_keys=True))
        else:
            md5.update(str(data))
    except:
        md5.update('')
    return md5.hexdigest()


def get_cache_dir(sub_name):
    path = os.path.join(config.CACHE_DIR, sub_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_time_info(fmt=None):
    timestamp = int(time.time())
    dt_str = None
    if fmt:
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt_str = dt.strftime(fmt)
    return timestamp, str(dt_str)


def iter_dir(path, suffix=None, exclude=[]):
    result = list()
    f_exclude = exclude
    if suffix:
        f_suffix = '.' + suffix
    if not os.path.isdir(path):
        return result
    for root, dirs, files in os.walk(path):
        for f in files:
            if suffix:
                if f.lower() in f_exclude:
                    continue
                if f.endswith(f_suffix):
                    result.append(f)
            else:
                result.append(f)
    return result
