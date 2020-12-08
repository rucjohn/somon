# _*_ coding:utf-8 _*_

import os
import json
import time
import winreg

from collector.utils import config

TASK = 'application'

HKLM = winreg.HKEY_LOCAL_MACHINE
HKCU = winreg.HKEY_CURRENT_USER
HKCR = winreg.HKEY_CLASSES_ROOT


def get_cache_dir():
    path = os.path.join(config.CACHE_DIR, TASK)
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


def iter_dir(path, suffix=None):
    result = list()
    f_exclude = ['setup.exe', 'uninstall.exe', 'uninst.exe', 'unins000.exe', 'liveupdate.exe']
    if suffix:
        f_suffix = '.' + suffix
    if not os.path.isdir(path):
        return result
    for root, dirs, files in os.walk(path):
        for f in files:
            if suffix:
                if f.lower() in f_exclude:
                    continue
                if f.endswith(f_suffix):
                    result.append(f)
            else:
                result.append(f)
    return result


def transfer(apps):
    result = list()
    for info in apps:
        display_name = info["DisplayName"]
        uninstall_string = info["UninstallString"]
        display_icon = info["DisplayIcon"]
        install_location = info["InstallLocation"]
        if display_name.lower().startswith('microsoft'):
            continue
        if uninstall_string.lower().startswith('msiexec.exe'):
            continue
        # if 'QQPCTray.exe' not in display_icon:
        #     continue
        if install_location and os.path.exists(install_location):
            location = os.path.dirname(install_location)
        elif display_icon:
            _icon = display_icon.split(',')[0]
            _icon = _icon.replace('"', '')
            location = os.path.dirname(_icon)
        else:
            _un_str = uninstall_string.split(',')[0]
            _un_str = _un_str.replace('"', ',')
            location = os.path.dirname(_un_str)
        relation_files = iter_dir(location, suffix='exe')
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
