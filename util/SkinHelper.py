#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
Author: AsherYang
Email:  ouyangfan1991@gmail.com
Date:   2018/7/10
Desc:   换肤工具类
"""

import sys
sys.path.append('../')
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QFile
from qss import style_rc


class SkinHelper:
    def __init__(self):
        pass

    def setStyle(self, widget, style_qss):
        qssFile = QFile(style_qss)
        qssFile.open(QFile.ReadOnly)
        # set style sheet
        styleSheet = qssFile.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        widget.setStyleSheet(styleSheet)
        qssFile.close()
