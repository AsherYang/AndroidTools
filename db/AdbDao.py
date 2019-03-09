#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : adb 数据库操作接口
"""

from bean.AdbBean import AdbBean
from util import DbUtil


class AdbDao:
    def __init__(self):
        pass

    def save(self, adbBean):
        if not adbBean or not isinstance(adbBean, AdbBean):
            return
        insert = 'insert into adb_cmds (adb_cmd_name, adb_cmd, adb_cmd_desc) ' \
                 'values("%s", "%s", "%s")' \
                 % (adbBean.adb_cmd_name, adbBean.adb_cmd, adbBean.adb_cmd_desc)
        return DbUtil.insert(insert)

    def delete(self, cmd):
        if not cmd:
            return
        delete = 'delete from adb_cmds where adb_cmd = "%s" ' % cmd
        return DbUtil.delete(delete)
