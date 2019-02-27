#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : windows WTS Session监听

https://blog.51cto.com/13723657/2108705
"""

import win32con
import win32gui
import win32ts

WM_WTSSESSION_CHANGE = 0x2B1
WTS_SESSION_LOCK = 0x7
WTS_SESSION_UNLOCK = 0x8


class WinWTSMonitor:
    def __init__(self, callBack=None):
        self.callBack = callBack
        self.className = "WTSMonitor"
        self.wndName = "WTS Event Monitor"
        wc = win32gui.WNDCLASS()
        wc.hInstance = hInst = win32gui.GetModuleHandle(None)
        wc.lpszClassName = self.className
        wc.lpfnWndProc = self.WndProc
        self.classAtom = win32gui.RegisterClass(wc)
        style = 0
        self.hWnd = win32gui.CreateWindow(self.classAtom, self.wndName,
                                          style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hInst, None)
        win32gui.UpdateWindow(self.hWnd)
        win32ts.WTSRegisterSessionNotification(self.hWnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

    def start(self):
        win32gui.PumpMessages()

    def stop(self):
        win32gui.PostQuitMessage(0)

    def WndProc(self, hWnd, message, wParam, lParam):
        if message == WM_WTSSESSION_CHANGE:
            self.OnSession(wParam, lParam)

    def OnSession(self, event, sessionID):
        # print '--> event: ', event
        # print '--> session: ', sessionID
        if self.callBack:
            self.callBack(event, sessionID)

    def __call__(self, *args, **kwargs):
        self.start()


if __name__ == '__main__':
    wtsMonitor = WinWTSMonitor()
    wtsMonitor.start()
