#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/20
Desc  : 字符串转换视图窗口
"""

from PyQt4 import QtGui, QtCore
from widget.StrTransformWidget import StrTransformWidget

class StrTransformView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()

        strTransformWidget = StrTransformWidget()

        mainLayout.addWidget(strTransformWidget)
        self.setLayout(mainLayout)
