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

    # 添加一条adb 指令
    def save(self, adbBean):
        if not adbBean or not isinstance(adbBean, AdbBean):
            return
        insert = 'insert into adb_cmds (adb_cmd_name, adb_cmd, adb_cmd_desc) ' \
                 'values("%s", "%s", "%s")' \
                 % (adbBean.adb_cmd_name, adbBean.adb_cmd, adbBean.adb_cmd_desc)
        return DbUtil.insert(insert)

    # 删除一条adb 指令
    def delete(self, cmd):
        if not cmd:
            return
        delete = 'delete from adb_cmds where adb_cmd = "%s" ' % cmd
        return DbUtil.delete(delete)

    # 查询所有添加的adb 指令
    def queryAll(self):
        query = 'SELECT * FROM adb_cmds;'
        resultList = DbUtil.query(query)
        # print resultList
        if not resultList:
            return None
        adbBeanList = []
        for row in resultList:
            # print row
            adbBean = AdbBean()
            row_id = row["_id"]
            adbBean.adb_cmd_name = row["adb_cmd_name"]
            adbBean.adb_cmd = row["adb_cmd"]
            adbBean.adb_cmd_desc = row["adb_cmd_desc"]
            adbBeanList.append(adbBean)
        return adbBeanList
