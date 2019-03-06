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

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class AdbOperateWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'adb指令')
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(300, 300)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 10, 5, 2)
        self.adbLineEdit = QtGui.QLineEdit()
        self.mainLayout.addWidget(self.adbLineEdit)
        self.centralwidget.setLayout(self.mainLayout)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    operAdbWin = AdbOperateWin()
    operAdbWin.show()
    sys.exit(app.exec_())
