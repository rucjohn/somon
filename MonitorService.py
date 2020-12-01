# _*_ coding:utf-8 _*_

import os
import sys
import time
import winerror
import win32timezone
import win32event
import win32service
import win32serviceutil
import servicemanager

import monitor


class SoMonService(win32serviceutil.ServiceFramework):

    _svc_name_ = 'SoMoService'
    _svc_display_name_ = 'SoMoService'
    _svc_description_ = 'Salt Monitor Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def SvcDoRun(self):
        while self.isAlive:
            monitor.collect()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False


if __name__ == '__main__':
    if len(sys.argv) != 1:
        win32serviceutil.HandleCommandLine(SoMonService)
    try:
        evt_src_dll = os.path.abspath(servicemanager.__file__)
        servicemanager.PrepareToHostSingle(SoMonService)
        servicemanager.Initialize('SoMonService', evt_src_dll)
        servicemanager.StartServiceCtrlDispatcher()
    except win32service.error as details:
        if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
            win32serviceutil.usage()
