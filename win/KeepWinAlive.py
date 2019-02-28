#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : 保持window 系统常亮

https://www.cnblogs.com/swarmbees/p/10046975.html
"""
import pyautogui as pag
import time
import threading

from util.DateUtil import DateUtil
from win.WinWTSMonitor import WinWTSMonitor, WTS_SESSION_LOCK, WTS_SESSION_UNLOCK

# https://blog.csdn.net/a1007720052/article/details/81215887?utm_source=blogxgwz5
pag.FAILSAFE = False

class KeepWinAlive:
    def __init__(self):
        # 需要防止类创建多次。pywintypes.error: (1410, 'RegisterClass', 'Class already exists.')
        self.wtsMonitor = WinWTSMonitor(self.wtsCallBack)
        self.oldx = 0
        self.oldy = 0
        self.prev_time = None
        self.cancel_status = False
        self.cancel_call_back = None

    def doKeepAlive(self):
        self.startMonitorScreen()
        thread = threading.Thread(target=self.keepAlive)
        thread.setDaemon(True)
        thread.start()

    def keepAlive(self):
        while not self.cancel_status:
            # 保持屏幕常亮功能
            # 获取鼠标坐标
            x, y = pag.position()
            # print 'x-> ' + str(x) + ' y -> ' + str(y)
            # print 'oldx-> ' + str(self.oldx) + ' oldy -> ' + str(self.oldy)
            now_time = DateUtil().getCurrentTime()

            if x == self.oldx and y == self.oldy:
                stay_seconds = (now_time - self.prev_time).seconds
                if stay_seconds >= 6:
                    self.prev_time = now_time
                    pag.click()
                    pag.moveTo(x + 10, y + 10, 0.1)
                    pag.moveTo(x, y, 0.1)
                    print u'>>> 模拟了一次鼠标移动'
                    # pag.press('esc')
                    # print u'模拟点击esc'
            else:
                # 更新旧坐标
                self.oldx = x
                self.oldy = y
                self.prev_time = now_time
            stay_seconds = (now_time - self.prev_time).seconds
            print "鼠标{%s}秒未移动" % stay_seconds
            pos_str = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
            # #打印坐标
            print pos_str
            time.sleep(2)

    def startMonitorScreen(self):
        thread = threading.Thread(target=self.wtsMonitor)
        thread.setDaemon(True)
        thread.start()

    def wtsCallBack(self, event, sessionId):
        if event == WTS_SESSION_LOCK:
            print 'wtsCallBack-- WTS_SESSION_LOCK'
            # 电脑锁屏后，也取消模拟点击，让电脑正常进入休眠。
            self.setCancelStatus(True)
        elif event == WTS_SESSION_UNLOCK:
            # self.loginStatus = True
            print 'wtsCallBack-- WTS_SESSION_UNLOCK----'

    # 外部控制循环接口
    def setCancelStatus(self, cancelStatus):
        self.cancel_status = cancelStatus
        self.doCallBackCancelStatus(cancelStatus=cancelStatus)

    # 回调取消状态
    def doCallBackCancelStatus(self, cancelStatus):
        if self.cancel_call_back:
            self.cancel_call_back(cancelStatus)

if __name__ == '__main__':
    keepAlive = KeepWinAlive()
    keepAlive.keepAlive()
