#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : other tools
"""

from PyQt4 import QtCore, QtGui

from util.EncodeUtil import _fromUtf8
from util import QSettingsUtil
from win.WinBootUp import WinBootUp


class SettingsWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.winBootUp = WinBootUp()

        mainLayout = QtGui.QVBoxLayout()
        commonGroupBox = QtGui.QGroupBox(_fromUtf8("&通用"))
        commonHBox = QtGui.QHBoxLayout()

        self.bootUpCB = QtGui.QCheckBox()
        bootUpLabel = QtGui.QLabel(_fromUtf8("开机启动"))
        self.bootUpCB.connect(self.bootUpCB, QtCore.SIGNAL('stateChanged(int)'), self.setBootUp)
        self.setBootUpBySetting()

        commonHBox.addWidget(self.bootUpCB)
        commonHBox.addWidget(bootUpLabel)
        commonHBox.addStretch(1)
        commonGroupBox.setLayout(commonHBox)

        mainLayout.addWidget(commonGroupBox)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def setBootUp(self):
        if self.bootUpCB.isChecked():
            QSettingsUtil.setBootUp(QSettingsUtil.bootUpOn)
            self.winBootUp.registerBootUp()
        else:
            QSettingsUtil.setBootUp(QSettingsUtil.bootUpOff)

    def setBootUpBySetting(self):
        bootUpStatus = QSettingsUtil.getBootUp()
        if bootUpStatus == QtCore.QString.number(QSettingsUtil.bootUpOn):
            self.bootUpCB.setChecked(True)
        else:
            self.bootUpCB.setChecked(False)

