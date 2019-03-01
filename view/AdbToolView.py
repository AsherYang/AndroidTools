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

        vSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        vSplitter.setStyleSheet("QSplitter::handle {background-color:rgb(195, 198, 204); margin-left:10px; margin-right:10px;}")
        vSplitter.setHandleWidth(1)
        vSplitter.addWidget(adbToolWidget)
        vSplitter.addWidget(logWidget)
        vSplitter.setStretchFactor(0, 6)
        vSplitter.setStretchFactor(1, 4)

        mainLayout.addWidget(vSplitter)
        self.setLayout(mainLayout)
