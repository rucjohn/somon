# _*_ coding:utf-8 _*_

import json
import time
import hashlib


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
