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


class OtherToolsWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        firstGroupBox = QtGui.QGroupBox(_fromUtf8("Windows"))
        firstHBox = QtGui.QHBoxLayout()

        lockScreenBtn = QtGui.QPushButton(_fromUtf8("电脑锁屏"))
        lockScreenAndOnBtn = QtGui.QPushButton(_fromUtf8("锁屏常亮"))
        lockScreenBtn.connect(lockScreenBtn, QtCore.SIGNAL('clicked()'), self.lockScreenBtnClick)
        lockScreenAndOnBtn.connect(lockScreenAndOnBtn, QtCore.SIGNAL('clicked()'), self.lockScreenAndOnBtnClick)

        firstHBox.addWidget(lockScreenBtn)
        firstHBox.addWidget(lockScreenAndOnBtn)
        firstHBox.addStretch(1)
        firstGroupBox.setLayout(firstHBox)

        mainLayout.addWidget(firstGroupBox)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    # 锁屏
    def lockScreenBtnClick(self):
        lockScreen = LockWinScreen()
        lockScreen.lock()

    # 锁屏并保持屏幕常亮
    def lockScreenAndOnBtnClick(self):
        self.lockScreenBtnClick()
        keepAlive = KeepWinAlive()
        keepAlive.doKeepAlive()
