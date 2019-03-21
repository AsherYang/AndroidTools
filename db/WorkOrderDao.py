#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : 工单 数据库操作接口
"""

from bean.WorkOrderBean import WorkOrderBean
from util import DbUtil


class WorkOrderDao:
    def __init__(self):
        pass

    # 添加一条工单处理信息
    def save(self, orderBean):
        if not orderBean or not isinstance(orderBean, WorkOrderBean):
            return
        insert = 'insert into work_oder (order_num, order_title, oder_reason, deal_time) ' \
                 'values("%s", "%s", "%s", "%s")' \
                 % (orderBean.order_num, orderBean.order_title, orderBean.order_reason, orderBean.deal_time)
        return DbUtil.insert(insert)

    # 删除一条工单处理信息
    def delete(self, orderBean):
        if not orderBean:
            return
        delete = 'delete from work_oder where order_num = "%s" ' % orderBean.order_num
        return DbUtil.delete(delete)

    # 查询所有添加的工单处理信息
    def queryAll(self):
        query = 'SELECT * FROM work_oder;'
        resultList = DbUtil.query(query)
        # print resultList
        if not resultList:
            return None
        workBeanList = []
        for row in resultList:
            # print row
            orderBean = WorkOrderBean()
            row_id = row["_id"]
            orderBean.order_num = row["order_num"]
            orderBean.order_title = row["order_title"]
            orderBean.order_reason = row["oder_reason"]
            orderBean.deal_time = row["deal_time"]
            workBeanList.append(orderBean)
        return workBeanList

    # 查询本周处理的工单信息
    def queryByWeek(self):
        query = 'SELECT * FROM work_oder where yearweek(date_format(deal_time, "%Y-%m-%d")) = yearweek(now());'
        resultList = DbUtil.query(query)
        # print resultList
        if not resultList:
            return None
        workBeanList = []
        for row in resultList:
            # print row
            orderBean = WorkOrderBean()
            row_id = row["_id"]
            orderBean.order_num = row["order_num"]
            orderBean.order_title = row["order_title"]
            orderBean.order_reason = row["oder_reason"]
            orderBean.deal_time = row["deal_time"]
            workBeanList.append(orderBean)
        return workBeanList
