#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : adb 工具
"""

import os
import platform
import re
from util.RunSysCommand import RunSysCommand
from util import FileUtil
from util.DateUtil import DateUtil
from util.EncodeUtil import _fromUtf8

# 判断系统类型
system = platform.system()
# print 'sys: ', system
# print os.environ
findCmd = None
if system is "Windows":
    findCmd = "findstr"
else:
    findCmd = "grep"

adbCmd = None
# 判断是否正确设置ANDROID_HOME环境变量
if 'ANDROID_HOME' in os.environ:
    if system is "Windows":
        adbCmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
    else:
        adbCmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
else:
    raise EnvironmentError(u'adb not found in environment path, please make sure ANDROID_HOME!')


class AdbUtil:
    def __init__(self):
        self._runSysCmd = RunSysCommand()
        self._serial_no = None
        self._lastScreenRecordPath = None

    # 获取设备列表(调用获取设备函数时，请使用adb 连接上手机，下同。)
    def getDeviceList(self):
        cmd = 'adb devices -l'
        # result = self.runSysCmd.run(cmd, should_process=False).stdout.read()
        reProductStr = r'product:(.+) model'
        reModelStr = r'model:(.+) device'
        reDeviceStr = r'device:(.+) transport_id'
        reTransportIdStr = r'transport_id:(.+)\r\n'
        devices = []
        result = self._runSysCmd.run(cmd, should_process=False).stdout.readlines()
        result.reverse()
        for device in result[1:]:
            if "attached" not in device.strip():
                deviceInfo = DeviceInfo()
                deviceInfo.serialNo = device.split(" ")[0]
                deviceInfo.product = re.findall(reProductStr, device)[0]
                deviceInfo.model = re.findall(reModelStr, device)[0]
                deviceInfo.device = re.findall(reDeviceStr, device)[0]
                deviceInfo.transportId = re.findall(reTransportIdStr, device)[0]
                devices.append(deviceInfo)
                # print '-->', deviceInfo
            else:
                break
        return devices

    # 获取当前设备序列
    def getCurrentSerialNo(self):
        deviceInfoList = self.getDeviceList()
        if len(deviceInfoList) == 1:
            self._serial_no = deviceInfoList[0].serialNo
        elif deviceInfoList:
            if self._serial_no is None:
                self._serial_no = deviceInfoList[0].serialNo
            else:
                serialNoList = []
                for device in deviceInfoList:
                    serialNoList.append(device.serialNo)
                if self._serial_no not in serialNoList:
                    self._serial_no = deviceInfoList[0].serialNo
        return self._serial_no

    # 设置当前设备序列号
    def setCurrentSerialNo(self, currentSerialNo):
        self._serial_no = currentSerialNo

    # 获取设备当前app包名
    def getDeviceTopPackageName(self):
        # -1: last one
        return self.getDeviceFocusedActivity().split('/')[0]

    # 获取设备当前Top Activity
    def getDeviceTopActivity(self):
        return self.getDeviceFocusedActivity().split('/')[-1]

    # 获取当前设备顶端activity信息
    def getDeviceFocusedActivity(self):
        cmd = str('%s -s %s shell dumpsys activity | %s mFocusedActivity' % (adbCmd, self.getCurrentSerialNo(), findCmd))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        # print cmd
        # print result
        # 不匹配 空格 : {
        reResultStr = r'[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+'
        return re.findall(reResultStr, result)[0]

    # 获取设备上所有APP 的包名
    def getDeviceAllPackage(self):
        cmd = str('%s -s %s shell pm list packages' % (adbCmd, self.getCurrentSerialNo()))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        return result

    # 向设备截屏
    def doScreenCap(self, deviceModel=None, callBack=None):
        screenPath = '/sdcard/screenshot_'
        if deviceModel:
            screenPath += deviceModel + "_"
        screenPath += str(DateUtil().getCurrentTimeStamp()) + ".png"
        destPath = "d:" + os.sep + "adbTools" + os.sep
        FileUtil.mkdirNotExist(destPath)
        cmd = str('%s -s %s shell /system/bin/screencap -p %s ' % (adbCmd, self.getCurrentSerialNo(), screenPath))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        if 'not found' in result:
            if callBack:
                callBack(_fromUtf8("未获取到设备, 请检查USB连接~"))
            return result
        cmd2 = str('%s -s %s pull %s %s' % (adbCmd, self.getCurrentSerialNo(), screenPath, destPath))
        result = self._runSysCmd.run(cmd2, should_process=False).stdout.read()
        if "file pulled" in result:
            # os.startfile('d:\\adbTools')
            self._runSysCmd.run(['explorer.exe', destPath])
        return result

    # 向设备录屏
    def doStartScreenRecord(self, deviceModel=None, callBack=None):
        recordPath = '/sdcard/demo_'
        if deviceModel:
            recordPath += deviceModel + "_"
        recordPath += str(DateUtil().getCurrentTimeStamp()) + ".mp4"
        self._lastScreenRecordPath = recordPath
        cmd = str('%s -s %s shell screenrecord %s' % (adbCmd, self.getCurrentSerialNo(), recordPath))
        callBack(_fromUtf8("正在进行录屏, 如需暂停请点击结束录屏按钮.."))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        if callBack and 'not found' in result:
            callBack(_fromUtf8("未获取到设备, 请检查USB连接~"))
        return result

    # 暂停录屏
    # https://stackoverflow.com/questions/25185746/stop-adb-screenrecord-from-java
    def doStopScreenRecord(self, callBack=None):
        if not self._lastScreenRecordPath:
            if callBack:
                callBack(_fromUtf8("请先进行录屏操作~"))
            return None
        recordPath = self._lastScreenRecordPath
        destPath = "d:" + os.sep + "adbTools" + os.sep
        FileUtil.mkdirNotExist(destPath)
        recordPidCmd = str('%s -s %s shell ps | %s screenrecord' % (adbCmd, self.getCurrentSerialNo(), findCmd))
        recordPidResult = self._runSysCmd.run(recordPidCmd, should_process=False).stdout.read()
        print 'recordRe: ', recordPidResult
        if 'not found' in recordPidResult:
            if callBack:
                callBack(_fromUtf8("未获取到设备, 请检查USB连接~"))
            return recordPidResult
        reRecordPidStr = r'[0-9]+'
        recordPid = re.findall(reRecordPidStr, recordPidResult)[0]
        print 'recordPid: ', recordPid
        killScreenRecordCmd = str('%s -s %s shell kill -2 %s' % (adbCmd, self.getCurrentSerialNo(), recordPid))
        self._runSysCmd.run(killScreenRecordCmd, should_process=False).stdout.read()
        cmd = str('%s -s %s pull %s %s' % (adbCmd, self.getCurrentSerialNo(), recordPath, destPath))
        result = self._runSysCmd.run(cmd, should_process=False).stdout.read()
        if "file pulled" in result:
            # os.startfile('d:\\adbTools')
            self._runSysCmd.run(['explorer.exe', destPath])
        return result


class DeviceInfo:
    def __init__(self):
        self._serial_no = None
        self._product = None
        self._model = None
        self._device = None
        self._transport_id = None

    @property
    def serialNo(self):
        return self._serial_no

    @serialNo.setter
    def serialNo(self, value):
        self._serial_no = value

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def transportId(self):
        return self._transport_id

    @transportId.setter
    def transportId(self, value):
        self._transport_id = value

    # toString
    def __str__(self):
        return 'serialNo: %s , product: %s ,  model: %s , device: %s , transportId: %s' \
               % (self.serialNo, self.product, self.model, self.device, self.transportId)


if __name__ == '__main__':
    adbUtil = AdbUtil()
    print 'focusActivity: ', adbUtil.getDeviceFocusedActivity()
    print 'packageName: ', adbUtil.getDeviceTopPackageName()
    print 'activityName: ', adbUtil.getDeviceTopActivity()
