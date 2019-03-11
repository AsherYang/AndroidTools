#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/23
Desc  : 程序使用 QSettings 保存配置类
doc @see: http://blog.csdn.net/loster_li/article/details/52841607

设置值，在window 可在注册表查找：
HKEY_USERS\S-1-5-21-1891589526-117931021-550679562-10201\Software\AsherYang\LAndroidTools\bootUpGroup
"""

from PyQt4 import QtCore

from constant import AppConstants

# 开机启动项配置
bootUpGroup = 'bootUpGroup'
bootUpKey = 'bootUpKey'
# 0: 不开机启动， 默认值
bootUpOff = 0
# 1：开机启动
bootUpOn = 1


def init():
    QtCore.QCoreApplication.setOrganizationName(AppConstants.OrganizationName)
    QtCore.QCoreApplication.setOrganizationDomain(AppConstants.OrganizationDomain)
    QtCore.QCoreApplication.setApplicationName(AppConstants.ApplicationName)


# 设置开机启动。 0：不开机启动，1：开机启动； 默认为0 不开机启动。
def setBootUp(value=0):
    setting = QtCore.QSettings()
    setting.beginGroup(bootUpGroup)
    setting.setValue(bootUpKey, value)
    setting.endGroup()
    setting.sync()


def getBootUp():
    setting = QtCore.QSettings()
    setting.beginGroup(bootUpGroup)
    bootUpValue = setting.value(bootUpKey, 0).toString()
    setting.endGroup()
    return bootUpValue
