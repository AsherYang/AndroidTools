#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/22
Desc  : 工单处理窗口
"""
from PyQt4 import QtGui, QtCore
from util.EncodeUtil import _fromUtf8
from util.DateUtil import DateUtil
from bean.WorkOrderBean import WorkOrderBean
from db.WorkOrderDao import WorkOrderDao
from util.QtFontUtil import QtFontUtil
import os
import threading
import xlwt


class WorkOrderWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.orderDao = WorkOrderDao()
        mainLayout = QtGui.QVBoxLayout()
        workOrderForm = QtGui.QFormLayout()
        operateHBox = QtGui.QHBoxLayout()

        orderNumLabel = QtGui.QLabel(_fromUtf8("工单号："))
        orderTitleLabel = QtGui.QLabel(_fromUtf8("工单标题："))
        orderReasonLabel = QtGui.QLabel(_fromUtf8("问题回复："))
        self.orderNumEdit = QtGui.QLineEdit()
        self.orderTitleEdit = QtGui.QLineEdit()
        self.orderReasonEdit = QtGui.QTextEdit()
        orderNumLabel.setMinimumHeight(25)
        orderTitleLabel.setMinimumHeight(25)
        orderReasonLabel.setMinimumHeight(25)
        self.orderNumEdit.setMinimumHeight(25)
        self.orderTitleEdit.setMinimumHeight(25)
        orderAddBtn = QtGui.QPushButton(_fromUtf8("增加"))
        orderDeleteBtn = QtGui.QPushButton(_fromUtf8("删除"))
        orderQueryWeekBtn = QtGui.QPushButton(_fromUtf8("导出本周"))
        orderQueryAllBtn = QtGui.QPushButton(_fromUtf8("导出所有"))
        orderAddBtn.connect(orderAddBtn, QtCore.SIGNAL('clicked()'), self.orderAddMethod)
        orderDeleteBtn.connect(orderDeleteBtn, QtCore.SIGNAL('clicked()'), self.orderDeleteMethod)
        orderQueryWeekBtn.connect(orderQueryWeekBtn, QtCore.SIGNAL('clicked()'), self.exportWeekData)
        orderQueryAllBtn.connect(orderQueryAllBtn, QtCore.SIGNAL('clicked()'), self.exportAllData)

        self.tipLabel = QtGui.QLabel()
        self.tipLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.tipLabel.setContentsMargins(5, 0, 5, 5)
        self.tipLabel.connect(self.tipLabel, QtCore.SIGNAL('tipsChangeSignal(QString)'), self.setTips)

        workOrderForm.addRow(orderNumLabel, self.orderNumEdit)
        workOrderForm.addRow(orderTitleLabel, self.orderTitleEdit)
        workOrderForm.addRow(orderReasonLabel, self.orderReasonEdit)
        operateHBox.addWidget(orderAddBtn)
        operateHBox.addWidget(orderDeleteBtn)
        operateHBox.addWidget(orderQueryWeekBtn)
        operateHBox.addWidget(orderQueryAllBtn)

        mainLayout.addLayout(workOrderForm)
        mainLayout.addSpacing(5)
        mainLayout.addLayout(operateHBox)
        mainLayout.addWidget(self.tipLabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def setTips(self, text):
        if text:
            self.tipLabel.setText(unicode(text))

    def orderAddMethod(self):
        orderNum = str(self.orderNumEdit.text()).decode('utf8')
        orderTitle = str(self.orderTitleEdit.text()).decode('utf8')
        orderReason = str(self.orderReasonEdit.toPlainText()).decode('utf8')
        orderDealTime = DateUtil().getCurrentTime()
        if not orderNum:
            self.setTips(_fromUtf8("添加工单信息时，工单号必不可少!"))
            return
        orderBean = WorkOrderBean()
        orderBean.order_num = orderNum
        orderBean.order_title = orderTitle
        orderBean.order_reason = orderReason
        orderBean.deal_time = orderDealTime
        result = self.orderDao.save(orderBean)
        if result:
            self.setTips(_fromUtf8("工单信息添加成功"))
        else:
            self.setTips(_fromUtf8("工单信息添加失败"))

    def orderDeleteMethod(self):
        orderNum = str(self.orderNumEdit.text()).decode('utf8')
        if not orderNum:
            return
        orderBean = WorkOrderBean()
        orderBean.order_num = orderNum
        result = self.orderDao.delete(orderBean)
        if result:
            self.setTips(_fromUtf8("工单信息删除成功"))
        else:
            self.setTips(_fromUtf8("工单信息删除失败"))

    def exportWeekData(self):
        thread = threading.Thread(target=self.orderQueryWeekMethod)
        thread.setDaemon(True)
        thread.start()

    def exportAllData(self):
        thread = threading.Thread(target=self.orderQueryAllMethod)
        thread.setDaemon(True)
        thread.start()

    # 导出本周数据
    def orderQueryWeekMethod(self):
        orderBeanList = self.orderDao.queryByWeek()
        if not orderBeanList:
            self.emitTipsChange(_fromUtf8("还没有工单信息~"))
            return
        excelPath = "C:\\Users\\20251572\\Desktop\\week_" + str(DateUtil().getCurrentTimeStamp()) + ".xls"
        self.write2Excel(orderBeanList, excelPath)
        os.startfile(excelPath)

    # 导出所有数据
    def orderQueryAllMethod(self):
        orderBeanList = self.orderDao.queryAll()
        if not orderBeanList:
            self.emitTipsChange(_fromUtf8("还没有工单信息~"))
            return
        excelPath = "C:\\Users\\20251572\\Desktop\\all_" + str(DateUtil().getCurrentTimeStamp()) + ".xls"
        self.write2Excel(orderBeanList, excelPath)
        os.startfile(excelPath)

    def write2Excel(self, orderList, path):
        if not orderList or not path:
            return
        workbook = xlwt.Workbook(encoding='utf-8')
        sheetData = workbook.add_sheet(u"工单信息")
        # 设置一下宽度
        for i in range(4):
            sheetData.col(i).width = 256*30
        sheetData.write(0, 0, u"工单号")
        sheetData.write(0, 1, u"工单标题")
        sheetData.write(0, 2, u"问题原因")
        sheetData.write(0, 3, u"处理时间")
        line = 1
        column = 0
        for orderBean in orderList:
            sheetData.write(line, column, orderBean.order_num)
            sheetData.write(line, column+1, orderBean.order_title)
            sheetData.write(line, column+2, orderBean.order_reason)
            sheetData.write(line, column+3, orderBean.deal_time)
            line += 1
            column = 0
        workbook.save(unicode(path))

    def emitTipsChange(self, tips):
        self.tipLabel.emit(QtCore.SIGNAL('tipsChangeSignal(QString)'), tips)

    def tipsChangeSignal(self, tips):
        pass