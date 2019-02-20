#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : 基础信息窗口

android apk基础信息：包名称，申明的权限，版本信息，等
"""

import sys
import threading

from PyQt4 import QtGui, QtCore

from util.AaptUtil import AaptUtil
from util.EncodeUtil import _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class BaseInfoWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        # base info apk 信息
        apkInfoGroupBox = QtGui.QGroupBox(_fromUtf8("apk信息"))
        apkInfoHBox = QtGui.QHBoxLayout()

        apkInfoLeftVBox = QtGui.QVBoxLayout()
        apkInfoMiddleVBox = QtGui.QVBoxLayout()
        apkInfoRightVBox = QtGui.QVBoxLayout()
        apkInfoForm = QtGui.QFormLayout()
        # formLayout 属性设置
        # Label 的对齐方式
        apkInfoForm.setLabelAlignment(QtCore.Qt.AlignRight)
        # form 的对齐方式
        # apkInfoForm.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        apkInfoForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # 表单一行的内容显示方式
        apkInfoForm.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        # field 域延伸方式
        apkInfoForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)

        self.apkInfoIcon = QtGui.QLabel()
        self.apkInfoAppName = QtGui.QLabel()
        self.apkInfoPackageName = QtGui.QLineEdit()
        self.apkInfoLauncherActivity = QtGui.QLineEdit()
        self.apkInfoVersionCode = QtGui.QLineEdit()
        self.apkInfoVersionName = QtGui.QLineEdit()
        self.apkInfoMinSdkVersion = QtGui.QLineEdit()
        self.apkInfoTargetSdkVersion = QtGui.QLineEdit()
        self.apkInfoPermissionList = QtGui.QTextEdit()
        # 设置鼠标可操作
        self.apkInfoAppName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        packageNameLabel = QtGui.QLabel()
        launcherActivityLabel = QtGui.QLabel()
        versionCodeLabel = QtGui.QLabel()
        versionNameLabel = QtGui.QLabel()
        minSdkVersionLabel = QtGui.QLabel()
        targetSdkVersionLabel = QtGui.QLabel()
        packageNameLabel.setText(_fromUtf8("包名称:"))
        launcherActivityLabel.setText(_fromUtf8("启动页:"))
        versionCodeLabel.setText(_fromUtf8("版本号:"))
        versionNameLabel.setText(_fromUtf8(" 版本名:"))
        minSdkVersionLabel.setText(_fromUtf8("最小SDK:"))
        targetSdkVersionLabel.setText(_fromUtf8("目标SDK:"))

        self.apkInfoAppName.connect(self.apkInfoAppName,
                                    QtCore.SIGNAL('updateAppInfoSignal(QString,QString,QString,QString,'
                                                  'QString,QString,QString,QString,QStringList)'),
                                    self.updateAppInfo)

        apkInfoForm.addRow(packageNameLabel, self.apkInfoPackageName)
        apkInfoForm.addRow(launcherActivityLabel, self.apkInfoLauncherActivity)
        apkInfoForm.addRow(versionCodeLabel, self.apkInfoVersionCode)
        apkInfoForm.addRow(versionNameLabel, self.apkInfoVersionName)
        apkInfoForm.addRow(minSdkVersionLabel, self.apkInfoMinSdkVersion)
        apkInfoForm.addRow(targetSdkVersionLabel, self.apkInfoTargetSdkVersion)
        apkInfoLeftVBox.addWidget(self.apkInfoIcon, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        apkInfoLeftVBox.addWidget(self.apkInfoAppName, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        apkInfoLeftVBox.addStretch(1)
        apkInfoMiddleVBox.addLayout(apkInfoForm)
        apkInfoMiddleVBox.setContentsMargins(5, 0, 5, 0)
        apkInfoRightVBox.addWidget(self.apkInfoPermissionList)
        apkInfoHBox.addLayout(apkInfoLeftVBox)
        apkInfoHBox.addLayout(apkInfoMiddleVBox)
        apkInfoHBox.addLayout(apkInfoRightVBox, 1)
        apkInfoGroupBox.setLayout(apkInfoHBox)

        mainLayout.addWidget(apkInfoGroupBox)
        self.setLayout(mainLayout)

    def analyApkInfoByThread(self, apkPath):
        thread = threading.Thread(target=self.analyApkInfoMethod, args=(apkPath,))
        thread.setDaemon(True)
        thread.start()

    def analyApkInfoMethod(self, apkPath):
        self.printLog(_fromUtf8("正在解析apk..."))
        aaptUtil = AaptUtil()
        apkInfo = aaptUtil.getApkInfo(apkPath)
        packageName = aaptUtil.getApkPackageName(apkPath, apkInfo)
        appLabel = aaptUtil.getApkApplicationLabel(apkPath, apkInfo)
        iconPath = aaptUtil.getApkApplicationIconPath(apkPath, apkInfo)
        launcherActivity = aaptUtil.getApkLauncherActivity(apkPath, apkInfo)
        versionCode = aaptUtil.getApkVersionCode(apkPath, apkInfo)
        versionName = aaptUtil.getApkVersionName(apkPath, apkInfo)
        minSdkVersion = aaptUtil.getApkMinSdkVersion(apkPath, apkInfo)
        targetSdkVersion = aaptUtil.getApkTargetSdkVersion(apkPath, apkInfo)
        permissionList = aaptUtil.getApkPermissionList(apkPath, apkInfo)

        self.emitUpdateAppInfoSignal(appLabel, iconPath, packageName, launcherActivity,
                                     versionCode, versionName, minSdkVersion, targetSdkVersion, permissionList)

    # 主线程中更新UI
    def updateAppInfo(self, appName, appIconPath, packageName, launcherActivity, versionCode, versionName,
                      minSdkVersion, targetSdkVersion, permissionList):
        self.apkInfoAppName.setText(appName)
        iconPixmap = QtGui.QPixmap(appIconPath)
        self.apkInfoIcon.setPixmap(iconPixmap)
        self.apkInfoPackageName.setText(packageName)
        self.apkInfoLauncherActivity.setText(launcherActivity)
        self.apkInfoVersionCode.setText(versionCode)
        self.apkInfoVersionName.setText(versionName)
        self.apkInfoMinSdkVersion.setText(minSdkVersion)
        self.apkInfoTargetSdkVersion.setText(targetSdkVersion)
        self.apkInfoPermissionList.setText(permissionList.join("\n"))
        self.printLog(_fromUtf8("apk解析完成"))

    def updateAppInfoSignal(self, appName, appIconPath, packageName, launcherActivity, versionCode, versionName,
                            minSdkVersion, targetSdkVersion, permissionList):
        pass

    def emitUpdateAppInfoSignal(self, appName, appIconPath, packageName, launcherActivity, versionCode, versionName,
                                minSdkVersion, targetSdkVersion, permissionList):
        self.apkInfoAppName.emit(QtCore.SIGNAL('updateAppInfoSignal(QString,QString,QString,QString,QString,'
                                               'QString,QString,QString, QStringList)'), appName, appIconPath, packageName,
                                 launcherActivity, versionCode, versionName, minSdkVersion, targetSdkVersion,permissionList)

    def printLog(self, log):
        self.emit(QtCore.SIGNAL('printLogSignal(QString)'), log)

    def printLogSignal(self, log):
        pass
