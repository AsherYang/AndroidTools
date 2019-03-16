#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/13
Desc  : 桌面小部件
"""
import sys

from PyQt4 import QtCore, QtGui

from util.EncodeUtil import _fromUtf8
from util.QtFontUtil import QtFontUtil


class DesktopWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.rightButton = False
        self.dragPos = 0
        self.initUI()
        # self.show()

    def initUI(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() / 20 * 16, screen.height() / 20 * 1, 350, 30)
        # we can resize the widget. https://blog.csdn.net/y673582465/article/details/73603265
        sizeGrip = QtGui.QSizeGrip(self)
        self.setWindowTitle('AndroidTools')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        quitAction = QtGui.QAction(_fromUtf8("退出"), self)
        quitAction.connect(quitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(quitAction)

        mainLayout = QtGui.QVBoxLayout()
        self.weatherlabel = QtGui.QLabel(_fromUtf8("天气"))
        self.weatherlabel.setPalette(QtFontUtil().setFontColor2Palette(QtCore.Qt.black))
        mainLayout.addWidget(self.weatherlabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
        tranColor = QtGui.QColor(0xDE, 0xDE, 0xDE)
        self.setTransparency(tranColor)

    def updateMsg(self, title, msg):
        pass

    def showWeather(self):
        pass

    def mouseReleaseEvent(self, event):
        if self.rightButton:
            self.rightButton = False
            self.popMenu.popup(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        if event.button() == QtCore.Qt.RightButton and not self.rightButton:
            self.rightButton = True

    # https://blog.csdn.net/seanyxie/article/details/5930779
    def setTransparency(self, color, p_float=0.5):
        p = self.palette()
        p.setColor(QtGui.QPalette.Background, color)
        self.setPalette(p)
        self.setWindowOpacity(p_float)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    desktopWidget = DesktopWidget()
    desktopWidget.show()
    sys.exit(app.exec_())
