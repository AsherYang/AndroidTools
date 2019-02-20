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
from util import SupportFiles


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
        self.connect(self, QtCore.SIGNAL('dropOpenFileSignal(QString)'), selectApkWidget.dropSrcFileSlot)

        mainLayout.addWidget(selectApkWidget)
        mainLayout.addSpacing(-10)
        # mainLayout.addStretch(1)
        mainLayout.addWidget(baseInfoWidget)
        mainLayout.addSpacing(-10)
        mainLayout.addWidget(logWidget)

        self.setLayout(mainLayout)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # http://www.iana.org/assignments/media-types/media-types.xhtml
        if event.mimeData().hasUrls() and event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                filePath = str(url.toLocalFile()).decode('utf-8')
                if SupportFiles.hasSupportFile(filePath):
                    event.acceptProposedAction()
                else:
                    print 'not accept this file!'
        else:
            print 'not accept this file too!'

    # 和 dragEnterEvent 结合使用，处理拖拽文件进窗口区域，进行打开。与右键和拖文件到桌面图标打开方式不同。
    # 本方式是在窗口打开的前提下，直接拖文件到窗口上，这种方式打开。
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filePath = str(url.toLocalFile()).decode('utf-8')
                # print filePath
                self.emit(QtCore.SIGNAL('dropOpenFileSignal(QString)'), filePath)
        return

    def dropOpenFileSignal(self, filePath):
        return
