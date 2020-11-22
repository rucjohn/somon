# _*_ coding:utf-8 _*_

import json
import psutil
import win32gui
import win32process

SYSTEM_CMD_KEYWORDS = ["Embedding"]
SYSTEM_NAME_KEYWORDS = ["System Idle Process", "host.exe", "broker.exe"]


def get_windows_text(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    titles = []
    win32gui.EnumWindows(callback, hwnds)
    for hwnd in hwnds:
        titles.append(win32gui.GetWindowText(hwnd))
    return titles


def transfer(processes):
    result = dict()
    for pid, info in processes.items():
        if not info['cmd']:
            continue
        if info['user'] == 'SYSTEM':
            continue
        if any([keyword in info['cmd'] for keyword in SYSTEM_CMD_KEYWORDS]):
            continue
        if any([keyword in info['name'] for keyword in SYSTEM_NAME_KEYWORDS]):
            continue
        result.update({pid: info})
    return result


def win():

    process_info = dict()
    for process in psutil.process_iter():
        info = dict()
        if process.pid is None:
            continue
        try:
            info['cmd'] = ' '.join(process.cmdline())
            info['name'] = process.name()
            info['user'] = process.username().split('\\')[-1]
            process_info[process.pid] = info
        except psutil.AccessDenied:
            continue

    return transfer(processes=process_info)


if __name__ == '__main__':
    ret = win()
    print(json.dumps(ret, indent=4))
    for pid in ret:
        print(pid, ret[pid]['name'], get_windows_text(pid))
