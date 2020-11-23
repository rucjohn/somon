# _*_ coding:utf-8 _*_

import os
import psutil


def pid_exists(pid):
    if not pid:
        return False
    if is_windows():
        import psutil
        if int(pid) in psutil.pids():
            return True
        return False
    else:
        path = os.path.join('/proc', pid)
        if os.path.exists(path):
            return True
        return False


class PID(object):
    def __init__(self, pid):
        self.pid = pid

    def exists(self):
        if not self.pid:
            return False
        if self.pid in psutil.pids():
            return True
        return False

    def kill(self):
        if self.pid:
            cmd = 'taskkill /f /pid {0}'.format(self.pid)
            os.popen(cmd)


