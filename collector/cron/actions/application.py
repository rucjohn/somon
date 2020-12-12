# _*_ coding:utf-8 _*_

import os
import json
import time
import winreg

from collector.utils import config, common

__TASK__ = 'APPLICATION'

HKLM = winreg.HKEY_LOCAL_MACHINE
HKCU = winreg.HKEY_CURRENT_USER
HKCR = winreg.HKEY_CLASSES_ROOT

CUSTOM_APPS = {
    "python.exe": "python",
    "explorer.exe": '文件资源管理器',
    "notepad.exe": '记事本',
    "Taskmgr.exe": '任务管理器',
    "cmd.exe": "命令提示符",
    "powershell.exe": 'Windows PowerShell',
    "WindowsTerminal.exe": 'Windows Terminal',
    "ctfmon.exe": 'Microsoft Office产品输入法可执行程序'
}


def get_cache_dir():
    path = os.path.join(config.CACHE_DIR, __TASK__)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def query_reg_subkey(psdrive, key=""):
    subkeys = []
    try:
        reg = winreg.OpenKey(psdrive, key)
        count = winreg.QueryInfoKey(reg)[0]
        for i in range(int(count)):
            name = winreg.EnumKey(reg, i)
            subkeys.append(name)
    except WindowsError:
        pass

    return subkeys


def query_reg_value(psdrive, key, sub_key):
    try:
        reg = winreg.OpenKey(psdrive, key)
        value, value_type_id = winreg.QueryValueEx(reg, sub_key)
    except WindowsError:
        value, value_type_id = ('', '')
    except TypeError:
        value, value_type_id = ('', '')

    return value, value_type_id


def query(psdriver, reg, query_fields):
    ret = list()
    query_key = query_reg_subkey(psdriver, reg)
    for _key in query_key:
        data = dict()
        final_key = os.path.join(reg, _key)
        for field in query_fields:
            value = query_reg_value(psdriver, final_key, field)[0]
            data.update({field: value})
        if not data["DisplayName"] or not data["UninstallString"]:
            continue
        ret.append(data)
    return ret


def transfer(apps):
    result = list()
    exclude = ['setup.exe', 'uninstall.exe', 'uninst.exe', 'unins000.exe', 'liveupdate.exe', "Update.exe", "cmd.exe"]
    for info in apps:
        display_name = info["DisplayName"]
        uninstall_string = info["UninstallString"]
        display_icon = info["DisplayIcon"]
        install_location = info["InstallLocation"]
        if display_name.lower().startswith('microsoft'):
            continue
        if uninstall_string.lower().startswith('msiexec.exe'):
            continue
        if install_location and os.path.exists(install_location):
            if os.path.isdir(install_location):
                location = install_location
            else:
                location = os.path.dirname(install_location)
        elif display_icon:
            _icon = display_icon.split(',')[0]
            _icon = _icon.replace('"', '')
            location = os.path.dirname(_icon)
        else:
            _un_str = uninstall_string.split(',')[0]
            _un_str = _un_str.replace('"', ',')
            location = os.path.dirname(_un_str)
        relation_files = common.iter_dir(location, suffix='exe', exclude=exclude)
        info.update({"format": {"location": location, "relation": relation_files}})
        result.append(info)
    return result


def win():
    apps = list()
    fields = ["DisplayName", "UninstallString", "DisplayIcon", "InstallLocation"]
    x64_reg = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    x86_reg = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    apps.extend(query(HKLM, x64_reg, fields))
    apps.extend(query(HKLM, x86_reg, fields))
    apps.extend(query(HKCU, x64_reg, fields))
    apps.extend(query(HKCU, x86_reg, fields))
    return apps


def responses():
    apps = win()
    return apps


def relation_responses():
    path = os.path.join(get_cache_dir(), 'relation_responses.txt')
    # 判断文件是否过期 > 30min
    if os.path.exists(path):
        mtime = int(os.stat(path).st_mtime)
        now = int(time.time())
        if now - mtime > 30 * 60:
            os.remove(path)
    if not os.path.exists(path):
        apps = win()
        result = transfer(apps=apps)
        with open(path, 'w') as f:
            f.write(json.dumps(result))
    else:
        with open(path, 'r') as f:
            result = json.loads(f.read())
    return result


if __name__ == '__main__':
    ret = relation_responses()
    print(json.dumps(ret, indent=4))
    # for app in ret:
    #     if app['DisplayName'] == '百度网盘':
    #         print(app)
