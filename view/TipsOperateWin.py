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
from constant import TipsType

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
        self.resize(350, 100)
        self.tipsDao = TipsDao()
        self.tipsList = []
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setContentsMargins(5, 10, 5, 2)
        operHBox = QtGui.QHBoxLayout()

        tipsForm = QtGui.QFormLayout()
        self.tipsTypeComboBox = QtGui.QComboBox()
        self.tipsDescEdit = QtGui.QLineEdit()
        self.tipsListEdit = QtGui.QTextEdit()
        self.tipsDescEdit.setPlaceholderText(_fromUtf8("输入提醒事项"))
        # tipsLayout = QtGui.QHBoxLayout()
        # tipsLayout.addWidget(self.tipsTypeComboBox, QtCore.Qt.AlignVCenter)
        # tipsLayout.addWidget(self.tipsDescEdit)
        # tipsForm.addRow(tipsLayout)
        tipsForm.addRow(self.tipsTypeComboBox, self.tipsDescEdit)
        self.tipsTypeComboBox.setMinimumHeight(25)
        self.tipsDescEdit.setMinimumHeight(25)
        self.addBtn = QtGui.QPushButton(_fromUtf8("添加"))
        self.deleteBtn = QtGui.QPushButton(_fromUtf8("删除"))
        self.queryBtn = QtGui.QPushButton(_fromUtf8("查询"))
        self.addBtn.connect(self.addBtn, QtCore.SIGNAL('clicked()'), self.doAddMethod)
        self.deleteBtn.connect(self.deleteBtn, QtCore.SIGNAL('clicked()'), self.doDeleteMethod)
        self.queryBtn.connect(self.queryBtn, QtCore.SIGNAL('clicked()'), self.doQueryMethod)
        self.tipLabel = QtGui.QLabel()
        self.tipLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.tipLabel.setContentsMargins(5, 0, 5, 5)
        self.setTipsType()
        operHBox.addWidget(self.addBtn, 1)
        operHBox.addWidget(self.deleteBtn, 1)
        operHBox.addWidget(self.queryBtn, 1)
        mainLayout.addLayout(tipsForm)
        mainLayout.addWidget(self.tipsListEdit)
        mainLayout.addSpacing(5)
        mainLayout.addLayout(operHBox)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.tipLabel)
        self.centralwidget.setLayout(mainLayout)

    def setTips(self, text):
        if text:
            self.tipLabel.setText(unicode(text))

    def setTipsType(self):
        tipType = TipsType.tips_type()
        if not tipType:
            return
        for type in tipType:
            self.tipsTypeComboBox.addItem(type)

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
            self.hasOperTipsList(tipBean.tips_desc, TipsOperateWin.operateAdd)
            self.emitOperTips()
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
            self.hasOperTipsList(tipsDesc, TipsOperateWin.operateDelete)
            self.emitOperTips()
        else:
            self.setTips(_fromUtf8("提醒事项删除失败, 请检查!"))

    def doQueryMethod(self):
        tipDap = TipsDao()
        tipsBeanList = tipDap.queryAll()
        if not tipsBeanList:
            self.setTips(_fromUtf8("请先添加提醒事项~"))
            return
        # 重新初始化
        self.tipsList[:] = []
        for tip in tipsBeanList:
            self.tipsList.append(unicode(tip.tips_desc))
        self.tipsListEdit.setText("\n".join(self.tipsList))

    # 响应 增删 操作
    def hasOperTipsList(self, tip_desc, operate):
        if not tip_desc or not self.tipsList:
            return
        if operate == TipsOperateWin.operateAdd:
            self.tipsList.append(unicode(tip_desc))
        elif operate == TipsOperateWin.operateDelete:
            self.tipsList.remove(tip_desc)
        self.tipsListEdit.setText("\n".join(self.tipsList))

    # 发送操作tips 改变的通知
    def emitOperTips(self):
        self.emit(QtCore.SIGNAL('operTipsSignal'))

    def operTipsSignal(self):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    operTipsWin = TipsOperateWin()
    operTipsWin.show()
    sys.exit(app.exec_())
