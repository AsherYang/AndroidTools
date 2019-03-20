#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/20
Desc  : 自定义图片按钮
"""
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap

class PixmapButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)

    def setPixmap(self, pixmap):
        pass
