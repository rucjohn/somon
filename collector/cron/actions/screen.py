# _*_ coding:utf-8 _*_

import os
import win32api
import win32ui
import win32gui


def capture(image_directory):
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    filename = 'foregroundWindow' + '.jpg'
    image_path = os.path.join(image_directory, filename)

    # 根据窗口句柄获取窗口的设备上下文DC（Device Context）
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # mfcDC创建可兼容的DC
    save_dc = mfc_dc.CreateCompatibleDC()
    # 创建bitmap准备保存图片
    save_bitmap = win32ui.CreateBitmap()
    # 获取监控器信息
    monitor_dev = win32api.EnumDisplayMonitors(None, None)
    length = monitor_dev[0][2][2]
    wide = monitor_dev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    save_bitmap.CreateCompatibleBitmap(mfc_dc, length, wide)
    # 高度saveDC，将截图保存到saveBitmap中
    save_dc.SelectObject(save_bitmap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    save_dc.BitBlt((0, 0), (length, wide), mfc_dc, (0, 0), win32con.SRCCOPY)
    # 保存图片
    save_bitmap.SaveBitmapFile(save_dc, image_path)