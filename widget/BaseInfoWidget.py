#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : 基础信息窗口

android apk基础信息：包名称，申明的权限，版本信息，等
"""

from PyQt4 import QtGui, QtCore
import sys
import threading
from util.QtFontUtil import QtFontUtil
from util.AaptUtil import AaptUtil
from util import FileUtil
from util.EncodeUtil import _translateUtf8, _fromUtf8

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class BaseInfoWidget(QtGui.QWidget):
    def __init__(self, parent=None, logCallBack=None):
        QtGui.QWidget.__init__(self, parent)
        self.logCallBack = logCallBack
        mainLayout = QtGui.QVBoxLayout()
        selectApkGroupBox = QtGui.QGroupBox(_fromUtf8("选择"))
        selectApkHBox = QtGui.QHBoxLayout()
        selectApkForm = QtGui.QFormLayout()
        self.srcApkLabel = QtGui.QLabel(_fromUtf8("源文件："))
        self.destApkLabel = QtGui.QLabel(_fromUtf8("目标文件："))
        self.srcApkEditHBox = QtGui.QHBoxLayout()
        self.destApkEditHBox = QtGui.QHBoxLayout()
        self.srcApkEdit = QtGui.QLineEdit()
        self.destApkEdit = QtGui.QLineEdit()
        self.srcApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))
        self.destApkScanBtn = QtGui.QPushButton(_fromUtf8("浏览.."))
        self.srcApkScanBtn.connect(self.srcApkScanBtn, QtCore.SIGNAL('clicked()'), self.scanSrcApkMethod)
        self.destApkScanBtn.connect(self.destApkScanBtn, QtCore.SIGNAL('clicked()'), self.scandestApkMethod)
        self.srcApkEdit.setTextMargins(10, 0, 10, 0)
        self.destApkEdit.setTextMargins(10, 0, 10, 0)
        self.srcApkLabel.setMinimumHeight(25)
        self.destApkLabel.setMinimumHeight(25)
        self.srcApkEdit.setMinimumHeight(25)
        self.destApkEdit.setMinimumHeight(25)
        self.srcApkScanBtn.setMinimumHeight(25)
        self.destApkScanBtn.setMinimumHeight(25)
        # formLayout 属性设置
        # Label 的对齐方式
        selectApkForm.setLabelAlignment(QtCore.Qt.AlignRight)
        # form 的对齐方式
        # selectApkForm.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        selectApkForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # 表单一行的内容显示方式
        selectApkForm.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        # field 域延伸方式
        selectApkForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)

        self.srcApkEditHBox.addWidget(self.srcApkEdit)
        self.srcApkEditHBox.addWidget(self.srcApkScanBtn)
        self.destApkEditHBox.addWidget(self.destApkEdit)
        self.destApkEditHBox.addWidget(self.destApkScanBtn)
        selectApkForm.addRow(self.srcApkLabel, self.srcApkEditHBox)
        selectApkForm.addRow(self.destApkLabel, self.destApkEditHBox)
        # selectApkForm.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.analyApkInfoBtn = QtGui.QPushButton(_fromUtf8("解析APK"))
        self.analyApkInfoBtn.setFixedSize(55, 55)
        self.analyApkInfoBtn.connect(self.analyApkInfoBtn, QtCore.SIGNAL('clicked()'), self.analyApkInfoByThread)

        selectApkHBox.addLayout(selectApkForm)
        selectApkHBox.addWidget(self.analyApkInfoBtn)
        selectApkGroupBox.setLayout(selectApkHBox)
        # base info apk 信息
        apkInfoGroupBox = QtGui.QGroupBox(_fromUtf8("apk信息"))
        apkInfoHBox = QtGui.QHBoxLayout()
        apkInfoLeftVBox = QtGui.QVBoxLayout()
        apkInfoMiddleVBox = QtGui.QVBoxLayout()
        apkInfoRightVBox = QtGui.QVBoxLayout()

        self.apkInfoIcon = QtGui.QLabel()
        self.apkInfoAppName = QtGui.QLabel()
        self.apkInfoPackageName = QtGui.QLineEdit()
        self.apkInfoLauncherActivity = QtGui.QLabel()
        self.apkInfoVersionCode = QtGui.QLabel()
        self.apkInfoVersionName = QtGui.QLabel()
        self.apkInfoMinSdkVersion = QtGui.QLabel()
        self.apkInfoTargetSdkVersion = QtGui.QLabel()

        self.apkInfoAppName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        # self.apkInfoPackageName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.apkInfoLauncherActivity.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.apkInfoVersionCode.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.apkInfoVersionName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.apkInfoMinSdkVersion.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.apkInfoTargetSdkVersion.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.apkInfoAppName.connect(self.apkInfoAppName,
                     QtCore.SIGNAL('updateAppInfoSignal(QString,QString,QString,QString,'
                                   'QString,QString,QString,QString)'),
                     self.updateAppInfo)

        apkInfoLeftVBox.addWidget(self.apkInfoIcon, 0, QtCore.Qt.AlignHCenter)
        apkInfoLeftVBox.addWidget(self.apkInfoAppName, 0, QtCore.Qt.AlignHCenter)
        apkInfoMiddleVBox.addWidget(self.apkInfoPackageName)
        apkInfoMiddleVBox.addWidget(self.apkInfoLauncherActivity)
        apkInfoMiddleVBox.addWidget(self.apkInfoVersionCode)
        apkInfoMiddleVBox.addWidget(self.apkInfoVersionName)
        apkInfoMiddleVBox.addWidget(self.apkInfoMinSdkVersion)
        apkInfoMiddleVBox.addWidget(self.apkInfoTargetSdkVersion)
        apkInfoHBox.addLayout(apkInfoLeftVBox)
        apkInfoHBox.addLayout(apkInfoMiddleVBox)
        apkInfoHBox.addStretch(1)
        apkInfoHBox.addLayout(apkInfoRightVBox)
        apkInfoGroupBox.setLayout(apkInfoHBox)

        mainLayout.addWidget(selectApkGroupBox)
        mainLayout.addWidget(apkInfoGroupBox)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def scanSrcApkMethod(self):
        filePath = unicode(QtGui.QFileDialog.getOpenFileName(None, u'选择文件', "D:\\", 'apk file(*.apk)'))
        if not filePath:
            return
        filePath = QtCore.QDir.toNativeSeparators(filePath)
        self.srcApkEdit.setText(filePath)
        destPath = FileUtil.getFilePathWithName(filePath)
        self.destApkEdit.setText(destPath)
        # FileUtil.mkdirNotExist(destPath)

    def scandestApkMethod(self):
        lastDir = self.destApkEdit.text() if self.destApkEdit.text() else "D:\\"
        dirPath = unicode(QtGui.QFileDialog.getExistingDirectory(None, u'选择文件夹', lastDir))
        dirPath = QtCore.QDir.toNativeSeparators(dirPath)
        if dirPath:
            self.destApkEdit.setText(dirPath)

    def analyApkInfoByThread(self):
        thread = threading.Thread(target=self.analyApkInfoMethod)
        thread.setDaemon(True)
        thread.start()

    def analyApkInfoMethod(self):
        apkPath = unicode(self.srcApkEdit.text())
        if not apkPath:
            self.logCallBack(_fromUtf8("请先选择需要解析的源apk..."))
            return
        self.logCallBack(_fromUtf8("正在解析apk..."))
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
                                     versionCode, versionName, minSdkVersion, targetSdkVersion)

    # 主线程中更新UI
    def updateAppInfo(self, appName, appIconPath, packageName,launcherActivity,versionCode,versionName,
                      minSdkVersion,targetSdkVersion):
        self.apkInfoAppName.setText(appName)
        iconPixmap = QtGui.QPixmap(appIconPath)
        self.apkInfoIcon.setPixmap(iconPixmap)
        self.apkInfoPackageName.setText(packageName)
        self.apkInfoLauncherActivity.setText(launcherActivity)
        self.apkInfoVersionCode.setText(versionCode)
        self.apkInfoVersionName.setText(versionName)
        self.apkInfoMinSdkVersion.setText(minSdkVersion)
        self.apkInfoTargetSdkVersion.setText(targetSdkVersion)

    def updateAppInfoSignal(self, appName, appIconPath, packageName,launcherActivity,versionCode,versionName,
                            minSdkVersion,targetSdkVersion):
        pass

    def emitUpdateAppInfoSignal(self, appName, appIconPath, packageName,launcherActivity,versionCode,versionName,
                                minSdkVersion,targetSdkVersion):
        self.apkInfoAppName.emit(QtCore.SIGNAL('updateAppInfoSignal(QString,QString,QString,QString,QString,'
                                               'QString,QString,QString)'), appName, appIconPath, packageName,
                                 launcherActivity, versionCode, versionName, minSdkVersion, targetSdkVersion)
