#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/03/06
Desc  :
"""

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSizePolicy, QWidget
from util.EncodeUtil import _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class AdbOperateWin(QtGui.QMainWindow):

    operateAdd = 1
    operateDelete = 2

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'adb指令')
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(300, 300)


        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setContentsMargins(5, 10, 5, 2)
        operHBox = QtGui.QHBoxLayout()

        self.adbLineEdit = QtGui.QLineEdit()
        self.sureBtn = QtGui.QPushButton(_fromUtf8("确定"))
        operHBox.addStretch()
        operHBox.addWidget(self.sureBtn)
        operHBox.addStretch()
        mainLayout.addWidget(self.adbLineEdit)
        mainLayout.addLayout(operHBox)
        self.centralwidget.setLayout(mainLayout)

    def setOperate(self, operate=operateAdd):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    operAdbWin = AdbOperateWin()
    operAdbWin.show()
    sys.exit(app.exec_())
