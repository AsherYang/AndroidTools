#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/21
Desc  : 字符串转换窗口
"""

import sys

from PyQt4 import QtCore, QtGui

from util.EncodeUtil import _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class StrTransformWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        srcStrGroupBox = QtGui.QGroupBox(_fromUtf8("源字符串"))
        operateGropBox = QtGui.QGroupBox(_fromUtf8("操作"))
        destStrGropBox = QtGui.QGroupBox(_fromUtf8("目标字符串"))

        srcStrHBox = QtGui.QHBoxLayout()
        operateHBox = QtGui.QHBoxLayout()
        destStrHBox = QtGui.QHBoxLayout()
        self.srcStrEdit = QtGui.QTextEdit()
        self.destStrEdit = QtGui.QTextEdit()
        srcStrHBox.addWidget(self.srcStrEdit)
        destStrHBox.addWidget(self.destStrEdit)
        # operate buttons
        self.operateAscii2UnicodeBtn = QtGui.QPushButton(_fromUtf8("Ascii转Unicode"))
        self.operateUnicode2AsciiBtn = QtGui.QPushButton(_fromUtf8("Unicode转Ascii"))
        self.operateUnicode2ChineseBtn = QtGui.QPushButton(_fromUtf8("Unicode转中文"))
        self.operateChinese2UnicodeBtn = QtGui.QPushButton(_fromUtf8("中文转Unicode"))
        self.operateUtf82ChineseBtn = QtGui.QPushButton(_fromUtf8("UTF8转中文"))
        self.operateChinese2Utf8Btn = QtGui.QPushButton(_fromUtf8("中文转UTF8"))
        self.operateUrlEncodeBtn = QtGui.QPushButton(_fromUtf8("URLEncode编码"))
        self.operateUrlDecodeBtn = QtGui.QPushButton(_fromUtf8("URLDecode解码"))
        self.operateAscii2UnicodeBtn.connect(self.operateAscii2UnicodeBtn, QtCore.SIGNAL('clicked()'), self.ascii2UnicodeBtnClick)
        self.operateUnicode2AsciiBtn.connect(self.operateUnicode2AsciiBtn, QtCore.SIGNAL('clicked()'), self.unicode2AsciiBtnClick)
        self.operateUnicode2ChineseBtn.connect(self.operateUnicode2ChineseBtn, QtCore.SIGNAL('clicked()'), self.unicode2ChineseBtnClick)
        self.operateChinese2UnicodeBtn.connect(self.operateChinese2UnicodeBtn, QtCore.SIGNAL('clicked()'), self.chinese2UnicodeBtnClick)
        self.operateUtf82ChineseBtn.connect(self.operateUtf82ChineseBtn, QtCore.SIGNAL('clicked()'), self.utf82ChineseBtnClick)
        self.operateChinese2Utf8Btn.connect(self.operateChinese2Utf8Btn, QtCore.SIGNAL('clicked()'), self.chinese2Utf8BtnClick)
        self.operateUrlEncodeBtn.connect(self.operateUrlEncodeBtn, QtCore.SIGNAL('clicked()'), self.urlEncodeBtnClick)
        self.operateUrlDecodeBtn.connect(self.operateUrlDecodeBtn, QtCore.SIGNAL('clicked()'), self.urlDecodeBtnClick)
        operateHBox.addWidget(self.operateAscii2UnicodeBtn)
        operateHBox.addWidget(self.operateUnicode2AsciiBtn)
        operateHBox.addWidget(self.operateUnicode2ChineseBtn)
        operateHBox.addWidget(self.operateChinese2UnicodeBtn)
        operateHBox.addWidget(self.operateUtf82ChineseBtn)
        operateHBox.addWidget(self.operateChinese2Utf8Btn)
        operateHBox.addWidget(self.operateUrlEncodeBtn)
        operateHBox.addWidget(self.operateUrlDecodeBtn)

        srcStrGroupBox.setLayout(srcStrHBox)
        operateGropBox.setLayout(operateHBox)
        destStrGropBox.setLayout(destStrHBox)

        mainLayout.addWidget(srcStrGroupBox, 1)
        mainLayout.addWidget(operateGropBox)
        mainLayout.addWidget(destStrGropBox, 1)
        self.setLayout(mainLayout)

    def clearEdit(self):
        self.srcStrEdit.clear()
        self.destStrEdit.clear()

    def ascii2UnicodeBtnClick(self):
        self.clearEdit()

    def unicode2AsciiBtnClick(self):
        self.clearEdit()

    def unicode2ChineseBtnClick(self):
        self.clearEdit()

    def chinese2UnicodeBtnClick(self):
        self.clearEdit()

    def utf82ChineseBtnClick(self):
        self.clearEdit()

    def chinese2Utf8BtnClick(self):
        self.clearEdit()

    def urlEncodeBtnClick(self):
        self.clearEdit()

    def urlDecodeBtnClick(self):
        self.clearEdit()

