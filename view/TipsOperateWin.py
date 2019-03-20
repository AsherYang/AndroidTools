#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/03/06
Desc  : 提醒信息操作窗口
"""

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget

from util.EncodeUtil import _fromUtf8
from util.QtFontUtil import QtFontUtil
from db.TipsDao import TipsDao
from bean.TipsBean import TipsBean

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class TipsOperateWin(QtGui.QMainWindow):

    operateAdd = 1
    operateDelete = 2

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'桌面提醒信息')
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(350, 200)
        self.tipsDao = TipsDao()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setContentsMargins(5, 10, 5, 2)
        operHBox = QtGui.QHBoxLayout()

        tipsForm = QtGui.QFormLayout()
        tipsTypeLabel = QtGui.QLabel(_fromUtf8("提醒类型:"))
        tipsDescLabel = QtGui.QLabel(_fromUtf8("提醒信息:"))
        self.tipsTypeComboBox = QtGui.QComboBox()
        self.tipsDescEdit = QtGui.QLineEdit()
        self.tipsDescEdit.setFixedHeight(25)
        tipsForm.addRow(tipsTypeLabel, self.tipsTypeComboBox)
        tipsForm.addRow(tipsDescLabel, self.tipsDescEdit)
        self.addBtn = QtGui.QPushButton(_fromUtf8("添加"))
        self.addBtn.setMinimumWidth(150)
        self.addBtn.connect(self.addBtn, QtCore.SIGNAL('clicked()'), self.doAddMethod)
        self.deleteBtn = QtGui.QPushButton(_fromUtf8("删除"))
        self.deleteBtn.setMinimumWidth(150)
        self.deleteBtn.connect(self.deleteBtn, QtCore.SIGNAL('clicked()'), self.doDeleteMethod)
        self.tipLabel = QtGui.QLabel()
        self.tipLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.tipLabel.setContentsMargins(5, 0, 5, 5)
        operHBox.addStretch()
        operHBox.addWidget(self.addBtn)
        operHBox.addSpacing(20)
        operHBox.addWidget(self.deleteBtn)
        operHBox.addStretch()
        mainLayout.addLayout(tipsForm)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(operHBox)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.tipLabel)
        self.centralwidget.setLayout(mainLayout)

    def setTips(self, text):
        if text:
            self.tipLabel.setText(unicode(text))

    def doAddMethod(self):
        tipsType = self.tipsTypeComboBox.currentText()
        tipsDesc = str(self.tipsDescEdit.text()).decode('utf8')
        # print 'tipsType:%s , tipsDesc:%s ' % (tipsType, tipsDesc)
        if not tipsDesc:
            self.setTips(_fromUtf8("提醒内容不能为空!"))
            return
        tipBean = TipsBean()
        tipBean.tips_type = tipsType
        tipBean.tips_desc = tipsDesc
        result = self.tipsDao.save(tipBean)
        if result:
            self.setTips(_fromUtf8("提醒事项添加加成功~"))
            self.emitOperateCmd(tipBean.tips_desc, TipsOperateWin.operateAdd)
        else:
            self.setTips(_fromUtf8("提醒事项添加失败, 请检查!"))

    def doDeleteMethod(self):
        tipsDesc = str(self.tipsDescEdit.text()).decode('utf8')
        if not tipsDesc:
            self.setTips(_fromUtf8("提醒内容不能为空!"))
            return
        result = self.tipsDao.delete(tipsDesc)
        if result:
            self.setTips(_fromUtf8("提醒事项已删除"))
            self.emitOperateCmd(tipsDesc, TipsOperateWin.operateDelete)
        else:
            self.setTips(_fromUtf8("提醒事项删除失败, 请检查!"))

    def emitOperateTips(self, tips, operation):
        self.emit(QtCore.SIGNAL('operateTipsSignal(QString, int)'), tips, operation)

    def operateTipsSignal(self, tips, operation):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    operTipsWin = TipsOperateWin()
    operTipsWin.show()
    sys.exit(app.exec_())
