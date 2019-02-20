#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/20
Desc  : LOG 显示区域
"""

from PyQt4 import QtGui
from PyQt4.QtGui import QSizePolicy

from util.EncodeUtil import _fromUtf8, _translateUtf8
from util.QtFontUtil import QtFontUtil


class LogWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        # show log
        self.logGroupBox = QtGui.QGroupBox(_fromUtf8("日志"))
        self.logHBox = QtGui.QHBoxLayout()
        self.logTextEdit = QtGui.QTextEdit()
        self.logTextEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logTextEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.logHBox.addWidget(self.logTextEdit)
        self.logGroupBox.setLayout(self.logHBox)

        mainLayout.addWidget(self.logGroupBox)
        self.setLayout(mainLayout)

    # LOG 显示
    def appendLog(self, logTxt):
        self.logTextEdit.append(_translateUtf8(logTxt))
