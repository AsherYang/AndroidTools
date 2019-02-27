#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : windows 锁屏
"""

from ctypes import windll


class LockWinScreen:

    def __init__(self):
        pass

    def lock(self):
        user32 = windll.LoadLibrary('user32.dll')
        user32.LockWorkStation()


if __name__ == '__main__':
    localScreen = LockWinScreen()
    localScreen.lock()
