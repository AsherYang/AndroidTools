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

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class BaseInfoWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

