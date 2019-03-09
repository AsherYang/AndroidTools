#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/22
Desc  : adb tool widget
"""

import threading

from PyQt4 import QtCore, QtGui

from util.AdbUtil import AdbUtil
from util.EncodeUtil import _fromUtf8
from view.AdbOperateWin import AdbOperateWin


class AdbToolWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.adbUtil = AdbUtil()
        self.operAdbWin = AdbOperateWin()
        self.deviceList = []
        mainLayout = QtGui.QVBoxLayout()
        devicesGroupBox = QtGui.QGroupBox(_fromUtf8("设备"))
        operateGroupBox = QtGui.QGroupBox(_fromUtf8("操作"))
        operationAdbListGroupBox = QtGui.QGroupBox(_fromUtf8("指令"))
        adbListGroupBox = QtGui.QGroupBox(_fromUtf8("常用指令集"))
        firstHBox = QtGui.QHBoxLayout()
        devicesHBox = QtGui.QHBoxLayout()
        addAdbListHBox = QtGui.QHBoxLayout()
        operateHBox = QtGui.QHBoxLayout()
        adbListHBox = QtGui.QHBoxLayout()

        self.getDevicesBtn = QtGui.QPushButton(_fromUtf8("获取设备"))
        self.getDevicesBtn.connect(self.getDevicesBtn, QtCore.SIGNAL('clicked()'), self.getDevicesBtnClick)
        self.getDevicesBtn.connect(self.getDevicesBtn, QtCore.SIGNAL('getDeviceSuccessSignal'), self.getDeviceSucess)
        self.devicesListComboBox = QtGui.QComboBox()
        self.devicesListComboBox.connect(self.devicesListComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'),
                                         self.deviceComboBoxCurrentChange)

        operListPackagesBtn = QtGui.QPushButton(_fromUtf8("APP包列表"))
        operScreenCapBtn = QtGui.QPushButton(_fromUtf8("截屏"))
        operStartScreenRecordBtn = QtGui.QPushButton(_fromUtf8("开始录屏"))
        operStopScreenRecordBtn = QtGui.QPushButton(_fromUtf8("结束录屏"))
        operListPackagesBtn.connect(operListPackagesBtn, QtCore.SIGNAL('clicked()'), self.operListPackageBtnClick)
        operScreenCapBtn.connect(operScreenCapBtn, QtCore.SIGNAL('clicked()'), self.operScreenCapBtnClick)
        operStartScreenRecordBtn.connect(operStartScreenRecordBtn, QtCore.SIGNAL('clicked()'), self.operStartScreenRecordBtnClick)
        operStopScreenRecordBtn.connect(operStopScreenRecordBtn, QtCore.SIGNAL('clicked()'), self.operStopScreenRecordBtnClick)

        operateAdbListBtn = QtGui.QPushButton(_fromUtf8("增删常用指令"))
        operateAdbListBtn.connect(operateAdbListBtn, QtCore.SIGNAL('clicked()'), self.operateAdbListBtnClick)

        # 显示常用指令集
        adbListEdit = QtGui.QTextEdit()

        devicesHBox.addWidget(self.getDevicesBtn)
        devicesHBox.addWidget(self.devicesListComboBox)

        operateHBox.addWidget(operListPackagesBtn)
        operateHBox.addWidget(operScreenCapBtn)
        operateHBox.addWidget(operStartScreenRecordBtn)
        operateHBox.addWidget(operStopScreenRecordBtn)

        addAdbListHBox.addWidget(operateAdbListBtn, 1)
        addAdbListHBox.addStretch(1)

        adbListHBox.addWidget(adbListEdit)

        devicesGroupBox.setLayout(devicesHBox)
        operationAdbListGroupBox.setLayout(addAdbListHBox)
        operateGroupBox.setLayout(operateHBox)
        adbListGroupBox.setLayout(adbListHBox)

        firstHBox.addWidget(devicesGroupBox, 1)
        firstHBox.addWidget(operationAdbListGroupBox, 1)

        mainLayout.addLayout(firstHBox)
        mainLayout.addWidget(operateGroupBox)
        mainLayout.addWidget(adbListGroupBox)

        self.setLayout(mainLayout)

    # 获取USB连接设备列表
    def getDevicesBtnClick(self):
        thread = threading.Thread(target=self.getDeviceList)
        thread.setDaemon(True)
        thread.start()

    # 操作常用指令(添加和删除)
    def operateAdbListBtnClick(self):
        self.operAdbWin.setTips(_fromUtf8("添加指令时,名称|描述(选填), 命令(必填)；删除指令时,填入命令即可。"))
        self.operAdbWin.show()

    # 获取设备上的APP包列表
    def operListPackageBtnClick(self):
        thread = threading.Thread(target=self.getPackageList)
        thread.setDaemon(True)
        thread.start()

    def operScreenCapBtnClick(self):
        deviceMode = None
        if self.devicesListComboBox.currentText():
            deviceMode = unicode(self.devicesListComboBox.currentText())
        thread = threading.Thread(target=self.adbUtil.doScreenCap, args=(deviceMode, self.doScreenCallBack,))
        thread.setDaemon(True)
        thread.start()

    def operStartScreenRecordBtnClick(self):
        deviceMode = None
        if self.devicesListComboBox.currentText():
            deviceMode = unicode(self.devicesListComboBox.currentText())
        print "deviceMode->> ", deviceMode
        thread = threading.Thread(target=self.adbUtil.doStartScreenRecord, args=(deviceMode, self.doScreenCallBack,))
        thread.setDaemon(True)
        thread.start()

    def operStopScreenRecordBtnClick(self):
        thread = threading.Thread(target=self.adbUtil.doStopScreenRecord,
                                  args=(self.doScreenCallBack,))
        thread.setDaemon(True)
        thread.start()

    def doScreenCallBack(self, msg):
        self.printLog(msg)

    def getDeviceList(self):
        deviceInfoList = self.adbUtil.getDeviceList()
        self.emitGetDeviceSuccess(deviceInfoList)

    def deviceComboBoxCurrentChange(self, currentText):
        if not currentText or not self.deviceList:
            return
        for deviceInfo in self.deviceList:
            if deviceInfo.model == currentText:
                self.adbUtil.setCurrentSerialNo(deviceInfo.serialNo)
                break

    # 获取设备APP 包
    def getPackageList(self):
        self.printLog(self.adbUtil.getDeviceAllPackage())

    def printLog(self, log):
        self.emit(QtCore.SIGNAL('printLogSignal(QString)'), log)

    def printLogSignal(self, log):
        pass

    def getDeviceSucess(self, deviceList):
        if not deviceList:
            self.printLog(_fromUtf8("未获取到设备, 请检查USB连接~"))
            return
        self.deviceList = deviceList
        for deviceInfo in deviceList:
            # 解决QComboBox重复添加的问题
            if self.devicesListComboBox.findText(deviceInfo.model) == -1:
                self.devicesListComboBox.addItem(deviceInfo.model)
                self.printLog(deviceInfo.serialNo)

    def getDeviceSuccessSignal(self, deviceList):
        pass

    def emitGetDeviceSuccess(self, deviceList):
        self.getDevicesBtn.emit(QtCore.SIGNAL('getDeviceSuccessSignal'), deviceList)

