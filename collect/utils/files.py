# _*_ coding:utf-8 _*_

import os


def gen_code(data):



def getsize(path, suffix=None):
    size = 0
    if not os.path.exists(path):
        return size
    if os.path.isdir(path):
        f_suffix = '.' + str(suffix)
        for root, dirs, files in os.walk(path):
            for f in files:
                if not f.endswith(f_suffix):
                    continue
                size += os.path.getsize(os.path.join(root, f))
    if os.path.isfile(path):
        size = os.path.getsize(path)
    return size


