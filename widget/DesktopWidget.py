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


class DesktopWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.rightButton = False
        self.dragPos = 0
        self.initUI()
        self.show()

    def initUI(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() / 20 * 17, screen.height() / 20 * 1, 200, 200)
        self.setWindowTitle('AndroidTools')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        quitAction = QtGui.QAction(_fromUtf8("退出"), self)
        quitAction.connect(quitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(quitAction)

        mainLayout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(_fromUtf8("ninnain"))
        mainLayout.addWidget(label)
        self.setLayout(mainLayout)
        self.setTransparency(QtCore.Qt.red, 0.2)

    def updateMsg(self):
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

    def setTransparency(self, color, p_float):
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        self.setWindowOpacity(p_float)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    desktopWidget = DesktopWidget()
    sys.exit(app.exec_())
