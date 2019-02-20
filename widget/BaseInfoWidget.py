#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : 基础信息窗口

android apk基础信息：包名称，申明的权限，版本信息，等
"""

from PyQt4 import QtGui, QtCore
import sys
from util.QtFontUtil import QtFontUtil
from util.EncodeUtil import _translateUtf8, _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class BaseInfoWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        self.selectSrcForm = QtGui.QFormLayout()
        self.srcApkLabel = QtGui.QLabel(_fromUtf8("源文件："))
        self.destApkLabel = QtGui.QLabel(_fromUtf8("目标文件："))
        self.srcApkEditHBox = QtGui.QHBoxLayout()
        self.destApkEditHBox = QtGui.QHBoxLayout()
        self.srcApkEdit = QtGui.QLineEdit()
        self.destApkEdit = QtGui.QLineEdit()
        self.srcApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))
        self.destApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))

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
        self.selectSrcForm.setLabelAlignment(QtCore.Qt.AlignRight)
        # form 的对齐方式
        # self.selectSrcForm.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.selectSrcForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # 表单一行的内容显示方式
        self.selectSrcForm.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        # field 域延伸方式
        self.selectSrcForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)

        self.srcApkEditHBox.addWidget(self.srcApkEdit)
        self.srcApkEditHBox.addWidget(self.srcApkScanBtn)
        self.destApkEditHBox.addWidget(self.destApkEdit)
        self.destApkEditHBox.addWidget(self.destApkScanBtn)
        self.selectSrcForm.addRow(self.srcApkLabel, self.srcApkEditHBox)
        self.selectSrcForm.addRow(self.destApkLabel, self.destApkEditHBox)
        # self.selectSrcForm.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        mainLayout.addLayout(self.selectSrcForm)
        self.setLayout(mainLayout)
