# _*_ coding:utf-8 _*_

import os
import sys
import logging
from collect.utils import file, common, config, process, logger

log = logger.get_logger('collect')


class Collect(object):

    def __init__(self):
        pass


class Main(object):

    def __init__(self):
        self.cache_dir = config.CACHE_DIR
        self.pid_path = os.path.join(self.cache_dir, 'collect.pid')
        self.md5_path = os.path.join(self.cache_dir, 'collect.md5')
        self.validate()

    def validate(self):
        # 检查缓存目录
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        # 检查进程
        proc = process.PID(pid=self.last_pid)
        if proc.exists():
            proc.kill()
            logging.info(u"{0} 进程存在, KILL! 任务重启!".format(self.last_pid))
            sys.exit(99)
        with open(self.pid_path, 'w') as f:
            f.write(str(self.pid))
        # 检查客户端版本
        logging.info(u"当前版本客户端: {0}".format(self.version))
        logging.info(u"上一版本客户端: {0}".format(self.last_version))
        if self.version != self.last_version:
            logging.info(u"客户端文件更新, 任务重启!")
            with open(self.md5_path, 'wb') as f:
                f.write(self.version)
            sys.exit(1)

    def run(self):
        self.finish()

    @property
    def version(self):
        path = os.path.dirname(os.path.realpath(__file__))
        value = common.gen_code(file.getsize(path, suffix='py'))
        return value

    @property
    def last_version(self):
        value = ''
        if os.path.exists(self.md5_path):
            with open(self.md5_path, 'r') as f:
                value = f.read()
        return value

    @property
    def pid(self):
        return os.getpid()

    @property
    def last_pid(self):
        value = None
        if os.path.exists(self.pid_path):
            with open(self.md5_path, 'r') as f:
                value = f.read()
        return value

    def finish(self):
        if os.path.exists(self.pid_path):
            os.remove(self.pid_path)


if __name__ == '_main__':
    app = Main()
    app.run()

