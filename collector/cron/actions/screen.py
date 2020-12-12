# _*_ coding:utf-8 _*_

import os
import time
import win32api
import win32con
import win32ui
import win32gui
from collector.utils import config

__TASK__ = 'SCREEN'
directory = os.path.join(config.CACHE_DIR, __TASK__)


def capture(image_directory=directory):
    # 图片存储
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    filename = str(int(time.time())) + '.jpg'
    image_path = os.path.join(image_directory, filename)
    # 获取最前端窗口
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    # 从配置中获取显示器分辨率
    width = config.SCREEN_WIDTH
    height = config.SCREEN_HEIGHT
    # 获取桌面
    desktop_hwnd = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(desktop_hwnd)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(save_bitmap)
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
    # 保存tup
    save_bitmap.SaveBitmapFile(mem_dc, image_path)
    # 释放内存
    mem_dc.DeleteDC()
    win32gui.DeleteObject(save_bitmap.GetHandle())
    # 打印最前端窗口
    return title


if __name__ == '__main__':
    while True:
        capture()
        time.sleep(10)

