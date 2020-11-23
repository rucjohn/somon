# _*_ coding:utf-8 _*_

import os
from collect.utils import file, common, config, process


if __name__ == '_main__':
    # 缓存目录
    if not os.path.exists(config.CACHE_DIR):
        os.makedirs(config.CACHE_DIR)
    # 缓存目录 - 相关路径
    pid_path = os.path.join(config.CACHE_DIR, 'collect.pid')
    md5_path = os.path.join(config.CACHE_DIR, 'collect.md5')
    # 获取当前客户端 MD5
    basedir = os.path.dirname(os.path.realpath(__file__))
    cur_version = common.gen_code(file.getsize(basedir, suffix='py'))
    # 获取缓存客户端 MD5
    last_version = ''
    if os.path.exists(md5_path):
        with open(md5_path, 'r') as f:
            last_version = f.read()
    # 获取缓存客户端 PID
    last_pid = None
    if os.path.exists(pid_path):
        with open(pid_path, 'r') as f:
            last_pid = f.read()
    # 判断进程是否存在
    proc = process.PID(pid=last_pid)
    if proc.exists():
        proc.kill()
    with open(pid_path, 'w') as f:
        f.write(str(os.getpgid()))


