#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : adb 数据库操作接口
"""

from bean.TipsBean import TipsBean
from util import DbUtil


class TipsDao:
    def __init__(self):
        pass

    # 添加一条提醒事项
    def save(self, tipsBean):
        if not tipsBean or not isinstance(tipsBean, TipsBean):
            return
        insert = 'insert into tips_today (tips_type, tips_desc) ' \
                 'values("%s", "%s")' \
                 % (tipsBean.tips_type, tipsBean.tips_desc)
        return DbUtil.insert(insert)

    # 删除一条提醒事项
    def delete(self, tips):
        if not tips:
            return
        delete = 'delete from tips_today where tips_desc = "%s" ' % tips
        return DbUtil.delete(delete)

    # 查询所有添加的提醒事项
    def queryAll(self):
        query = 'SELECT * FROM tips_today;'
        resultList = DbUtil.query(query)
        # print resultList
        if not resultList:
            return None
        tipsBeanList = []
        for row in resultList:
            # print row
            tipsBean = TipsBean()
            row_id = row["_id"]
            tipsBean.tips_type = row["tips_type"]
            tipsBean.tips_desc = row["tips_desc"]
            tipsBeanList.append(tipsBean)
        return tipsBeanList
