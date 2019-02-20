#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/20
Desc  : base info 视图窗口

"""

from PyQt4 import QtGui, QtCore

from widget.BaseInfoWidget import BaseInfoWidget
from widget.LogWidget import LogWidget
from widget.SelectApkWidget import SelectApkWidget


class BaseInfoView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()

        selectApkWidget = SelectApkWidget()
        baseInfoWidget = BaseInfoWidget()
        logWidget = LogWidget()

        selectApkWidget.connect(selectApkWidget, QtCore.SIGNAL('analyApkInfoSignal(QString)'),
                                baseInfoWidget.analyApkInfoByThread)
        SelectApkWidget.connect(selectApkWidget, QtCore.SIGNAL('printLogSignal(QString)'), logWidget.appendLog)
        baseInfoWidget.connect(baseInfoWidget, QtCore.SIGNAL('printLogSignal(QString)'), logWidget.appendLog)

        mainLayout.addWidget(selectApkWidget)
        mainLayout.addSpacing(-10)
        # mainLayout.addStretch(1)
        mainLayout.addWidget(baseInfoWidget)
        mainLayout.addSpacing(-10)
        mainLayout.addWidget(logWidget)

        self.setLayout(mainLayout)
