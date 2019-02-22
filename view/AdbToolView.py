#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/22
Desc  : adb tool view
"""
from PyQt4 import QtGui, QtCore
from widget.AdbToolWidget import AdbToolWidget
from widget.LogWidget import LogWidget


class AdbToolView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        adbToolWidget = AdbToolWidget()
        logWidget = LogWidget()

        adbToolWidget.connect(adbToolWidget, QtCore.SIGNAL('printLogSignal(QString)'), logWidget.appendLog)

        mainLayout.addWidget(adbToolWidget)
        mainLayout.addWidget(logWidget)
        self.setLayout(mainLayout)
