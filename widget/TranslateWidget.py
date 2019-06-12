#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/6/5
Desc  : 翻译widget
"""

from PyQt4 import QtGui, QtCore
from util.TranslateUtil import Translate


class TranslateWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.translate = Translate()
        mainLayout = QtGui.QVBoxLayout()
        srcStrLayout = QtGui.QHBoxLayout()
        destStrLayout = QtGui.QHBoxLayout()
        operBtnsLayout = QtGui.QHBoxLayout()
        self.srcStrEdit = QtGui.QTextEdit()
        self.destStrEdit = QtGui.QTextEdit()
        self.translateBtn = QtGui.QPushButton(u'翻译')
        self.voiceBtn = QtGui.QPushButton(u'发音')
        self.translateBtn.setFixedSize(100, 30)
        self.voiceBtn.setFixedSize(100, 30)
        self.translateBtn.connect(self.translateBtn, QtCore.SIGNAL('clicked()'), self.translateBtnClick)
        srcStrLayout.addWidget(self.srcStrEdit)
        destStrLayout.addWidget(self.destStrEdit)
        operBtnsLayout.addStretch(1)
        operBtnsLayout.addWidget(self.translateBtn)
        operBtnsLayout.addWidget(self.voiceBtn)
        mainLayout.addLayout(srcStrLayout, 1)
        mainLayout.addLayout(destStrLayout, 1)
        mainLayout.addLayout(operBtnsLayout)
        self.setLayout(mainLayout)

    def translateBtnClick(self):
        srcText = unicode(self.srcStrEdit.toPlainText())
        if not srcText:
            return
        result = self.translate.translate(srcText)
        if not result:
            return
        str = ''
        for res in result:
            str += res
        self.destStrEdit.setText(str)
