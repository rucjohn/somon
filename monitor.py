# _*_ coding:utf-8 _*_

import os
import sys
import platform
import logging
import subprocess


def collect(task):
    logging.info(u"启动scheduler: Collect")
    basedir = os.path.dirname(os.path.abspath(__file__))
    collect_dir = os.path.join(basedir, 'collect')
    try:
        os.chdir(collect_dir)
    except OSError:
        return False
    if not os.path.exists('main.py'):
        logging.info(u"调用主进程失败")
        return False
    logging.info(u"调用主进程")
    cmd = r'c:\salt\bin\python.exe main.py {0}'.format(task)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return True
