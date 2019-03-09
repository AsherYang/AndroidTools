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
from PyQt4.QtGui import QWidget

from util.EncodeUtil import _fromUtf8
from util.QtFontUtil import QtFontUtil
from db.AdbDao import AdbDao
from bean.AdbBean import AdbBean

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
        self.resize(350, 200)
        self.adbDao = AdbDao()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setContentsMargins(5, 10, 5, 2)
        operHBox = QtGui.QHBoxLayout()

        adbCmdForm = QtGui.QFormLayout()
        adbCmdNameLabel = QtGui.QLabel(_fromUtf8("adb名称:"))
        adbCmdLabel = QtGui.QLabel(_fromUtf8("adb命令:"))
        adbCmdDescLabel = QtGui.QLabel(_fromUtf8("adb描述:"))
        self.adbCmdNameEdit = QtGui.QLineEdit()
        self.adbCmdEdit = QtGui.QLineEdit()
        self.adbCmdDescEdit = QtGui.QLineEdit()
        self.adbCmdNameEdit.setFixedHeight(25)
        self.adbCmdEdit.setFixedHeight(25)
        self.adbCmdDescEdit.setFixedHeight(25)
        adbCmdForm.addRow(adbCmdNameLabel, self.adbCmdNameEdit)
        adbCmdForm.addRow(adbCmdLabel, self.adbCmdEdit)
        adbCmdForm.addRow(adbCmdDescLabel, self.adbCmdDescEdit)
        self.addBtn = QtGui.QPushButton(_fromUtf8("添加"))
        self.addBtn.setMinimumWidth(150)
        self.addBtn.connect(self.addBtn, QtCore.SIGNAL('clicked()'), self.doAddAdbMethod)
        self.deleteBtn = QtGui.QPushButton(_fromUtf8("删除"))
        self.deleteBtn.setMinimumWidth(150)
        self.deleteBtn.connect(self.deleteBtn, QtCore.SIGNAL('clicked()'), self.doDeleteAdbMethod)
        self.tipLabel = QtGui.QLabel()
        self.tipLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.tipLabel.setContentsMargins(5, 0, 5, 5)
        operHBox.addStretch()
        operHBox.addWidget(self.addBtn)
        operHBox.addSpacing(20)
        operHBox.addWidget(self.deleteBtn)
        operHBox.addStretch()
        mainLayout.addLayout(adbCmdForm)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(operHBox)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.tipLabel)
        self.centralwidget.setLayout(mainLayout)

    def setTips(self, text):
        if text:
            self.tipLabel.setText(unicode(text))

    def doAddAdbMethod(self):
        adbCmdName = str(self.adbCmdNameEdit.text()).decode('utf8')
        adbCmd = str(self.adbCmdEdit.text()).decode('utf8')
        adbCmdDesc = str(self.adbCmdDescEdit.text()).decode('utf8')
        print 'adbCmdName:%s , adbCmd:%s , adbCmdDesc: %s ' % (adbCmdName, adbCmd, adbCmdDesc)
        if not adbCmd:
            self.setTips(_fromUtf8("adb命令不能为空!"))
            return
        adbBean = AdbBean()
        adbBean.adb_cmd_name = adbCmdName
        adbBean.adb_cmd = adbCmd
        adbBean.adb_cmd_desc = adbCmdDesc
        result = self.adbDao.save(adbBean)
        if result:
            self.setTips(_fromUtf8("adb命令添加加成功~"))
        else:
            self.setTips(_fromUtf8("adb命令添加失败, 请检查!"))

    def doDeleteAdbMethod(self):
        adbCmdName = str(self.adbCmdNameEdit.text()).decode('utf8')
        adbCmd = str(self.adbCmdEdit.text()).decode('utf8')
        adbCmdDesc = str(self.adbCmdDescEdit.text()).decode('utf8')
        print 'adbCmdName:%s , adbCmd:%s , adbCmdDesc: %s ' % (adbCmdName, adbCmd, adbCmdDesc)
        if not adbCmd:
            self.setTips(_fromUtf8("adb命令不能为空!"))
            return
        result = self.adbDao.delete(adbCmd)
        if result:
            self.setTips(_fromUtf8("adb命令已删除"))
        else:
            self.setTips(_fromUtf8("adb命令删除失败, 请检查!"))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    operAdbWin = AdbOperateWin()
    operAdbWin.show()
    sys.exit(app.exec_())
