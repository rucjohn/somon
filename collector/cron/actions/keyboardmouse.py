# _*_ coding:utf-8 _*_

import os
import json

from collector.utils import config, common

__TASK__ = 'KM'
keyboard_dir = os.path.join(config.CACHE_DIR, 'KEYBOARD')
mouse_dir = os.path.join(config.CACHE_DIR, 'MOUSE')


def count(path):
    with open(path, 'r') as fd:
        content = fd.readlines()
    result = dict(
        start=int(os.path.getctime(path)),
        end=int(os.path.getmtime(path)),
        count=len(content),
        content=[x.strip() for x in content]
    )
    return result


def summary(task):
    result = []
    per_count = 20
    subdir = os.path.join(config.CACHE_DIR, task)
    relation_files = common.iter_dir(subdir)
    if len(relation_files) == 1:
        return result
    # 没次统计PRE_COUNT
    relation_files.sort()
    if len(relation_files) >= per_count + 1:
        relation_files = relation_files[:per_count]
    else:
        relation_files = relation_files[:-1]
    if not relation_files:
        return result
    # 统计
    for name in relation_files:
        path = os.path.join(subdir, name)
        info = count(path)
        result.append(info)
    return result


def win():
    result = dict(
        mouse=summary(task='MOUSE'),
        keyboard=summary(task='KEYBOARD')
    )
    return result


def response():
    return win()


if __name__ == '__main__':
    ret = win()
    print(json.dumps(ret, indent=4))
