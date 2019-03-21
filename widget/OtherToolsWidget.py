#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : other tools
"""

from PyQt4 import QtCore, QtGui
from util.EncodeUtil import _fromUtf8
from win.LockWinScreen import LockWinScreen
from win.KeepWinAlive import KeepWinAlive
from widget.DesktopWidget import DesktopWidget
from widget.WorkOrderWidget import WorkOrderWidget
from view.TipsOperateWin import TipsOperateWin


class OtherToolsWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.keepAlive = KeepWinAlive()
        self.tipsWin = TipsOperateWin()
        self.keepAlive.cancel_call_back = self.keepWinCancelCallBack
        self.desktopWidget = DesktopWidget()
        mainLayout = QtGui.QVBoxLayout()
        firstGroupBox = QtGui.QGroupBox(_fromUtf8("Windows"))
        firstHBox = QtGui.QHBoxLayout()
        secondGroupBox = QtGui.QGroupBox(_fromUtf8("Work"))
        secondHBox = QtGui.QHBoxLayout()
        # container Widget
        containerGroupBox = QtGui.QGroupBox(_fromUtf8(""))
        containerHBox = QtGui.QHBoxLayout()
        self.containerWidget = QtGui.QStackedWidget()

        lockScreenBtn = QtGui.QPushButton(_fromUtf8("电脑锁屏"))
        self.keepScreenOnBtn = QtGui.QPushButton(_fromUtf8("电脑常亮"))
        cancelScreeOnBtn = QtGui.QPushButton(_fromUtf8("取消常亮"))
        showDesktopWidgetBtn = QtGui.QPushButton(_fromUtf8("显示窗口小部件"))
        tipsOperateBtn = QtGui.QPushButton(_fromUtf8("提醒信息"))
        workOrderBtn = QtGui.QPushButton(_fromUtf8("工单处理"))
        todoListBtn = QtGui.QPushButton(_fromUtf8("todoList"))
        lockScreenBtn.connect(lockScreenBtn, QtCore.SIGNAL('clicked()'), self.lockScreenBtnClick)
        self.keepScreenOnBtn.connect(self.keepScreenOnBtn, QtCore.SIGNAL('clicked()'), self.keepScreenOnBtnClick)
        cancelScreeOnBtn.connect(cancelScreeOnBtn, QtCore.SIGNAL('clicked()'), self.cancelScreenOnBtnClick)
        showDesktopWidgetBtn.connect(showDesktopWidgetBtn, QtCore.SIGNAL('clicked()'), self.showDesktopWidget)
        tipsOperateBtn.connect(tipsOperateBtn, QtCore.SIGNAL('clicked()'), self.showTipsOperateWin)
        self.tipsWin.connect(self.tipsWin, QtCore.SIGNAL('operTipsSignal'), self.changeTipsList)
        workOrderBtn.connect(workOrderBtn, QtCore.SIGNAL('clicked()'), self.showWorkOrderWidget)
        todoListBtn.connect(todoListBtn, QtCore.SIGNAL('clicked()'), self.showTodoListWidget)

        firstHBox.addWidget(lockScreenBtn)
        firstHBox.addWidget(self.keepScreenOnBtn)
        firstHBox.addWidget(cancelScreeOnBtn)
        firstHBox.addWidget(showDesktopWidgetBtn)
        firstHBox.addWidget(tipsOperateBtn)
        firstHBox.addStretch(1)
        firstGroupBox.setLayout(firstHBox)

        secondHBox.addWidget(workOrderBtn)
        secondHBox.addWidget(todoListBtn)
        secondHBox.addStretch(1)
        secondGroupBox.setLayout(secondHBox)

        # self.containerWidget.addWidget(self.tipsWin)
        containerHBox.addWidget(self.containerWidget)
        containerGroupBox.setLayout(containerHBox)
        mainLayout.addWidget(firstGroupBox)
        mainLayout.addWidget(secondGroupBox)
        mainLayout.addStretch(3)
        mainLayout.addWidget(containerGroupBox, 1)
        self.setLayout(mainLayout)

    # 锁屏
    def lockScreenBtnClick(self):
        lockScreen = LockWinScreen()
        lockScreen.lock()

    # 保持屏幕常亮
    def keepScreenOnBtnClick(self):
        # self.lockScreenBtnClick()
        self.keepAlive.doKeepAlive()
        # 防止重复点击创造多个线程
        # self.keepScreenOnBtn.setEnabled(False)
        # 也可以通过设置 cancelStatus 来反向回调，控制按钮点击状态
        self.keepAlive.setCancelStatus(False)

    def cancelScreenOnBtnClick(self):
        self.keepAlive.setCancelStatus(True)

    def keepWinCancelCallBack(self, cancel_status):
        self.keepScreenOnBtn.setEnabled(cancel_status)

    # 防止多次创建 wtsMonitor
    def setWinWTSMonitor(self, wtsMonitor):
        self.keepAlive.setWinWTSMonitor(wtsMonitor)

    def showDesktopWidget(self):
        self.desktopWidget.showWeather(self.desktopWidget.getWeather())
        self.desktopWidget.addWeatherJob()
        self.desktopWidget.addTipsJoB()
        self.desktopWidget.show()

    def showTipsOperateWin(self):
        self.tipsWin.setTips(_fromUtf8("添加删除时，需填写相关的提醒事项~"))
        # self.tipsWin.show()
        self.containerWidget.addWidget(self.tipsWin)
        self.containerWidget.setCurrentWidget(self.tipsWin)

    def showWorkOrderWidget(self):
        workOrderWidget = WorkOrderWidget()
        self.containerWidget.addWidget(workOrderWidget)
        self.containerWidget.setCurrentWidget(workOrderWidget)

    def showTodoListWidget(self):
        pass

    def changeTipsList(self):
        self.desktopWidget.queryTipsMethod()
