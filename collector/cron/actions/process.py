# _*_ coding:utf-8 _*_

import json
import copy
import psutil
import win32gui
import win32process
from collector.cron.actions import application

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
        if 'WindowsApps' in info['cmd'] or 'SystemApps' in info['cmd']:
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


def response():
    # EXE对应所有程序
    app_dict = dict()
    app_dict.update(application.CUSTOM_APPS)
    apps = application.relation_responses()
    for app in apps:
        for name in app['format']['relation']:
            app_dict[name] = app['DisplayName']
    # EXE对应进程
    proc_dict = win()
    for pid, proc in proc_dict.items():
        proc_dict[pid]['app'] = app_dict.get(proc['name'])
        proc_dict[pid]['window_text'] = get_windows_text(pid)

    return proc_dict


if __name__ == '__main__':
    ret = response()
    # print(json.dumps(ret, indent=4))
    for pid, proc in ret.items():
        print(pid, proc['name'], proc['app'], proc['window_text'])
    # print(json.dumps(ret, indent=4))
    # for pid in ret:
    #     print(pid, ret[pid]['name'], get_windows_text(pid))
