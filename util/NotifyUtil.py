#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/26
Desc  : notify util
"""

# import notify2
import platform
from win10toast import ToastNotifier
from util.IconResourceUtil import resource_path

system = platform.system()


class NotifyUtil:
    def __init__(self):
        pass

    def notify(self):
        if system is "Windows":
            self.notifyWin()
        else:
            self.notifyUnix()

    def notifyWin(self, title="Hello Asher", message="AndroidTools msg",
                  icon_path=resource_path('../android_tools_logo.ico'), time_out=10):
        toaster = ToastNotifier()
        toaster.show_toast(title=title, msg=message, icon_path=icon_path, duration=time_out)

    def notifyUnix(self, title="Hello Asher", message="AndroidTools msg",
                   icon_path=resource_path('../android_tools_logo.ico'), time_out=10000):
        icon = icon_path
        # notify2.init("AndroidTools")
        # n = notify2.Notification(summary=title, message=message, icon=icon)
        # n.set_urgency(notify2.URGENCY_NORMAL)
        # n.set_timeout(time_out)
        # n.show()


if __name__ == '__main__':
    notifyUtil = NotifyUtil()
    notifyUtil.notify()
