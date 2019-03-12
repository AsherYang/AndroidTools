#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/11
Desc  : 添加开机启动注册表

http://yshblog.com/blog/132
"""

import win32api

import win32con

from constant import AppConstants
from util import FileUtil
from win import WinCommandEnCoding


class WinBootUp:
    def __init__(self):
        self.name = AppConstants.ApplicationName
        winOsArgv = WinCommandEnCoding.getOsArgv()
        # self.exePath = "D:\\develope_demo\\github\\AndroidTools\\dist\\AndroidTools.exe"
        # 对于打开终端来说，所携带参数为第1位(打开文件的地址)，第0位为本执行程序地址
        self.exePath = winOsArgv[0]
        self.bootUpkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    # 注册开机启动项
    def registerBootUp(self):
        if FileUtil.getFileName(self.exePath) == "python.exe":
            return
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, self.bootUpkey, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, self.name, 0, win32con.REG_SZ, self.exePath)
            win32api.RegCloseKey(key)
            print 'register boot success!'
        except:
            print 'register boot up key error !'

    def unRegisterBootUp(self):
        if FileUtil.getFileName(self.exePath) == "python.exe":
            return
        try:
            key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, self.bootUpkey, 0, win32con.KEY_ALL_ACCESS)
            # self.name 是值的名称
            win32api.RegDeleteValue(key, self.name)
            win32api.RegCloseKey(key)
            print 'unRegister boot success!'
        except:
            print 'unRegister boot up key error !'


if __name__ == '__main__':
    winBootUp = WinBootUp()
    # winBootUp.registerBootUp()
    winBootUp.unRegisterBootUp()
