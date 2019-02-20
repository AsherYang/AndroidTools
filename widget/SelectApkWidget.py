#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : 选择apk窗口

"""

import sys

from PyQt4 import QtGui, QtCore

from util import FileUtil
from util.EncodeUtil import _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class SelectApkWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        selectApkGroupBox = QtGui.QGroupBox(_fromUtf8("选择"))
        selectApkHBox = QtGui.QHBoxLayout()
        selectApkForm = QtGui.QFormLayout()
        self.srcApkLabel = QtGui.QLabel(_fromUtf8("源文件："))
        self.destApkLabel = QtGui.QLabel(_fromUtf8("目标文件："))
        self.srcApkEditHBox = QtGui.QHBoxLayout()
        self.destApkEditHBox = QtGui.QHBoxLayout()
        self.srcApkEdit = QtGui.QLineEdit()
        self.destApkEdit = QtGui.QLineEdit()
        self.srcApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))
        self.destApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))
        self.srcApkScanBtn.connect(self.srcApkScanBtn, QtCore.SIGNAL('clicked()'), self.scanSrcApkMethod)
        self.destApkScanBtn.connect(self.destApkScanBtn, QtCore.SIGNAL('clicked()'), self.scanDestApkMethod)
        self.srcApkEdit.setTextMargins(10, 0, 10, 0)
        self.destApkEdit.setTextMargins(10, 0, 10, 0)
        self.srcApkLabel.setMinimumHeight(25)
        self.destApkLabel.setMinimumHeight(25)
        self.srcApkEdit.setMinimumHeight(25)
        self.destApkEdit.setMinimumHeight(25)
        self.srcApkScanBtn.setMinimumHeight(25)
        self.destApkScanBtn.setMinimumHeight(25)
        # formLayout 属性设置
        # Label 的对齐方式
        selectApkForm.setLabelAlignment(QtCore.Qt.AlignRight)
        # form 的对齐方式
        # selectApkForm.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        selectApkForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # 表单一行的内容显示方式
        selectApkForm.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        # field 域延伸方式
        selectApkForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)

        self.srcApkEditHBox.addWidget(self.srcApkEdit)
        self.srcApkEditHBox.addWidget(self.srcApkScanBtn)
        self.destApkEditHBox.addWidget(self.destApkEdit)
        self.destApkEditHBox.addWidget(self.destApkScanBtn)
        selectApkForm.addRow(self.srcApkLabel, self.srcApkEditHBox)
        selectApkForm.addRow(self.destApkLabel, self.destApkEditHBox)
        # selectApkForm.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.analyApkInfoBtn = QtGui.QPushButton(_fromUtf8("解析APK"))
        self.analyApkInfoBtn.setFixedSize(55, 55)
        self.analyApkInfoBtn.connect(self.analyApkInfoBtn, QtCore.SIGNAL('clicked()'), self.analyApkInfoBtnClick)

        selectApkHBox.addLayout(selectApkForm)
        selectApkHBox.addWidget(self.analyApkInfoBtn)
        selectApkGroupBox.setLayout(selectApkHBox)

        mainLayout.addWidget(selectApkGroupBox)
        self.setLayout(mainLayout)

    def scanSrcApkMethod(self):
        filePath = unicode(QtGui.QFileDialog.getOpenFileName(None, u'选择文件', "D:\\", 'apk file(*.apk)'))
        self.setEditByApkPath(filePath)

    def scanDestApkMethod(self):
        lastDir = self.destApkEdit.text() if self.destApkEdit.text() else "D:\\"
        dirPath = unicode(QtGui.QFileDialog.getExistingDirectory(None, u'选择文件夹', lastDir))
        dirPath = QtCore.QDir.toNativeSeparators(dirPath)
        if dirPath:
            self.destApkEdit.setText(dirPath)

    def setEditByApkPath(self, filePath):
        if not filePath:
            return
        filePath = QtCore.QDir.toNativeSeparators(filePath)
        self.srcApkEdit.setText(filePath)
        destPath = FileUtil.getFilePathWithName(filePath)
        self.destApkEdit.setText(destPath)
        # FileUtil.mkdirNotExist(destPath)

    def analyApkInfoBtnClick(self):
        apkPath = unicode(self.srcApkEdit.text())
        if not apkPath:
            self.printLog(_fromUtf8("请先选择需要解析的源apk..."))
            return
        self.emit(QtCore.SIGNAL('analyApkInfoSignal(QString)'), apkPath)

    def analyApkInfoSignal(self, apkPath):
        pass

    def printLog(self, log):
        self.emit(QtCore.SIGNAL('printLogSignal(QString)'), log)

    def printLogSignal(self, log):
        pass

    # 接收拖拽文件的槽函数
    def dropSrcFileSlot(self, apkPath):
        filePath = unicode(apkPath)
        self.setEditByApkPath(filePath)
        self.analyApkInfoBtn.click()
