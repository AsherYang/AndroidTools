#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/6/5
Desc  : copyFile widget
"""

from PyQt4 import QtGui, QtCore

from util.EncodeUtil import _fromUtf8, _translateUtf8
from util.ThreadUtil import ThreadUtil
from util.ZipFileUtil import ZipFileUtil

class UnzipFileWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        operBtnsLayout = QtGui.QHBoxLayout()
        filePathForm = QtGui.QFormLayout()

        srcFilePathLabel = QtGui.QLabel(_fromUtf8("文件目录："))
        self.srcFilePathEdit = QtGui.QLineEdit()
        self.logEdit = QtGui.QTextEdit()

        srcFilePathLabel.setMinimumHeight(25)
        self.srcFilePathEdit.setMinimumHeight(25)

        self.unzipFileBtn = QtGui.QPushButton(u'解压文件')
        self.unzipFileBtn.setFixedSize(100, 30)
        self.unzipFileBtn.connect(self.unzipFileBtn, QtCore.SIGNAL('clicked()'), self.unzipFileBtnClick)
        self.logEdit.connect(self.logEdit, QtCore.SIGNAL('appendLogSignal(QString)'), self.appendLog)

        filePathForm.addRow(srcFilePathLabel, self.srcFilePathEdit)
        operBtnsLayout.addStretch(1)
        operBtnsLayout.addWidget(self.unzipFileBtn)
        mainLayout.addLayout(filePathForm)
        mainLayout.addWidget(self.logEdit)
        mainLayout.addLayout(operBtnsLayout)
        self.setLayout(mainLayout)

    # copy file
    def unzipFileBtnClick(self):
        srcFilePath = str(self.srcFilePathEdit.text())
        if not srcFilePath:
            tips = unicode("请输入解压目录")
            self.setTips(_fromUtf8(tips))
            return
        # 解压文件
        threadUtil = ThreadUtil(funcName=self.doUnzipFile, srcFilePath=srcFilePath, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    def doUnzipFile(self, srcFilePath, log_call_back):
        zipFileUtil = ZipFileUtil(log_call_back)
        zipFileUtil.recursiveUnZipFile(srcFilePath)
        log_call_back(u'解压完成')

    # 显示操作日志
    def appendLog(self, logTxt):
        self.logEdit.append(_translateUtf8(logTxt))

    # 解决在子线程中刷新UI 的问题。' QWidget::repaint: Recursive repaint detected '
    def appendLogSignal(self, logTxt):
        pass

    def emitAppendLogSignal(self, logTxt):
        self.logEdit.emit(QtCore.SIGNAL('appendLogSignal(QString)'), logTxt)
