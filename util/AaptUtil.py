#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : aapt 工具类
"""

import os
import platform
import re
import zipfile
from util import FileUtil
from util.RunSysCommand import RunSysCommand
from util.EncodeUtil import _fromUtf8, _translateUtf8

# 判断系统类型
system = platform.system()
# print 'sys: ', system
# print os.environ
findCmd = None
if system is "Windows":
    findCmd = "findstr"
else:
    findCmd = "grep"

aaptCmd = None
# 判断是否正确设置ANDROID_HOME环境变量
if 'ANDROID_HOME' in os.environ:
    if system is "Windows":
        buildToolsPath = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
        pathList = FileUtil.getSubDir(buildToolsPath)
        aaptCmd = os.path.join(pathList[0], 'aapt.exe')
    else:
        buildToolsPath = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
        pathList = FileUtil.getSubDir(buildToolsPath)
        aaptCmd = os.path.join(pathList[0], 'aapt')
else:
    raise EnvironmentError(u'adb not found in environment path, please make sure ANDROID_HOME!')


class AaptUtil:
    def __init__(self):
        self._runSysCmd = RunSysCommand()

    # 获取apk 包名(调用获取apk信息函数时，是直接解析apk文件的，下同。)
    def getApkPackageName(self, apkPath, apkInfo=None):
        # cmd = str('%s dump badging %s | %s package' % (aaptCmd, apkPath, findCmd))
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'package: name=\'([a-zA-Z0-9\.]+)'
        apkPackageNameList = re.findall(reResultStr, apkInfo)
        if apkPackageNameList:
            return apkPackageNameList[0]
        return u'未获取到包名'

    # 获取apk启动的activity
    def getApkLauncherActivity(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'launchable-activity: name=\'([a-zA-Z0-9\.]+)'
        launchActivityList = re.findall(reResultStr, apkInfo)
        if launchActivityList:
            return launchActivityList[0]
        return u'未获取到启动页'

    # 获取apk 版本号
    def getApkVersionCode(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'versionCode=\'([a-zA-Z0-9\.]+)'
        versionCodeList = re.findall(reResultStr, apkInfo)
        if versionCodeList:
            return versionCodeList[0]
        return u'未获取到versionCode'

    def getApkVersionName(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'versionName=\'([a-zA-Z0-9\.]+)'
        versionNameList = re.findall(reResultStr, apkInfo)
        if versionNameList:
            return versionNameList[0]
        return u'未获取到versionName'

    # 获取apk 目标设备sdk版本
    def getApkMinSdkVersion(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'sdkVersion.\'([a-zA-Z0-9\.]+)'
        minSdkVersionList = re.findall(reResultStr, apkInfo)
        if minSdkVersionList:
            return minSdkVersionList[0]
        return u'未获取到最小SDK版本'

    def getApkTargetSdkVersion(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'targetSdkVersion.\'([a-zA-Z0-9\.]+)'
        targetSdkVersionList = re.findall(reResultStr, apkInfo)
        if targetSdkVersionList:
            return targetSdkVersionList[0]
        return u'未获取到适配SDK版本'

    # 获取apk 标签名
    def getApkApplicationLabel(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reApplicationInfoStr = r'application: label=.+'
        applicationInfo = re.findall(reApplicationInfoStr, apkInfo)[0]
        reResultStr = u"application: label=\'([a-zA-Z0-9\u4e00-\u9fa5\.]+)"
        applicationLabelList = re.findall(reResultStr, unicode(_translateUtf8(applicationInfo)))
        if applicationLabelList:
            return applicationLabelList[0]
        return u'未获取到应用名'

    # 获取apk 图标在apk中存在的路径
    def getApkApplicationIconPathInApk(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reApplicationInfoStr = r'application: label=.+'
        applicationInfo = re.findall(reApplicationInfoStr, apkInfo)[0]
        reResultStr = r'icon=\'([a-zA-Z0-9_/\-\.]+)'
        applicationIconInApkList = re.findall(reResultStr, applicationInfo)
        if applicationIconInApkList:
            return applicationIconInApkList[0]
        return None

    # 获取apk 图标路径，若不存在，则将图片写入apk包名命名的文件夹，文件为：icon_launcher.png
    def getApkApplicationIconPath(self, apkPath, apkInfo=None):
        apkPath = unicode(apkPath)
        applicationIconStr = self.getApkApplicationIconPathInApk(apkPath, apkInfo)
        if not applicationIconStr:
            return u'未获取到应用图标'
        apkZip = zipfile.ZipFile(apkPath)
        iconData = apkZip.read(applicationIconStr)
        iconDestPath = FileUtil.getFilePathWithName(apkPath)
        FileUtil.mkdirNotExist(iconDestPath)
        saveIconPath = os.path.join(iconDestPath, 'icon_launcher.png')
        if FileUtil.isFileOrDirExist(saveIconPath):
            return saveIconPath
        with open(saveIconPath, 'w+b') as saveIcon:
            saveIcon.write(iconData)
        return saveIconPath

    # 获取apk 使用权限列表
    def getApkPermissionList(self, apkPath, apkInfo=None):
        if apkInfo is None:
            apkInfo = self.getApkInfo(apkPath)
        reResultStr = r'uses-permission.\'([a-zA-Z0-9_\.\-]+)'
        return re.findall(reResultStr, apkInfo)

    # 获取apk 信息
    def getApkInfo(self, apkPath):
        cmd = str('%s dump badging %s' % (aaptCmd, apkPath))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        return result

if __name__ == '__main__':
    aaptUtil = AaptUtil()
    print aaptUtil.getApkInfo('C:\\Users\\20251572\\Desktop\\XTCLauncher.apk')
    # print aaptUtil.getApkPackageName('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkLauncherActivity('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkVersionCode('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkVersionName('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkMinSdkVersion('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkTargetSdkVersion('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkApplicationLabel('F:\\nexus6p\\nexus6p_backup\\MobileAssistant_1.apk')
    # print aaptUtil.getApkApplicationIconPathInApk('F:\\nexus6p\\nexus6p_backup\\tv.danmaku.bili_5.34.1_5341000.apk')
    # print aaptUtil.getApkApplicationIconPath('F:\\nexus6p\\nexus6p_backup\\tv.danmaku.bili_5.34.1_5341000.apk')
    # print aaptUtil.getApkPermissionList('F:\\nexus6p\\nexus6p_backup\\tv.danmaku.bili_5.34.1_5341000.apk')
