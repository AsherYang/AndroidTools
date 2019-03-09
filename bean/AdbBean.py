#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : adb 数据实体
"""


class AdbBean:
    def __init__(self):
        self._adb_cmd_name = None
        self._adb_cmd = None
        self._adb_cmd_desc = None

    @property
    def adb_cmd_name(self):
        return self._adb_cmd_name

    @adb_cmd_name.setter
    def adb_cmd_name(self, cmd_name):
        self._adb_cmd_name = cmd_name

    @property
    def adb_cmd(self):
        return self._adb_cmd

    @adb_cmd.setter
    def adb_cmd(self, cmd):
        self._adb_cmd = cmd

    @property
    def adb_cmd_desc(self):
        return self._adb_cmd_desc

    @adb_cmd_desc.setter
    def adb_cmd_desc(self, cmd_desc):
        self._adb_cmd_desc = cmd_desc

    def __str__(self):
        return "cmd_name: %s, cmd: %s , cmd_desc: %s" % (self._adb_cmd_name, self._adb_cmd, self._adb_cmd_desc)
