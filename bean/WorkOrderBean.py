#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : 工单信息 数据实体
"""


class WorkOrderBean:
    def __init__(self):
        self._order_num = None
        self._order_title = None
        self._order_reason = None
        self._deal_time = None

    @property
    def order_num(self):
        return self._order_num

    @order_num.setter
    def order_num(self, order_num):
        self._order_num = order_num

    @property
    def order_title(self):
        return self._order_title

    @order_title.setter
    def order_title(self, order_title):
        self._order_title = order_title

    @property
    def order_reason(self):
        return self._order_reason

    @order_reason.setter
    def order_reason(self, order_reason):
        self._order_reason = order_reason

    @property
    def deal_time(self):
        return self._deal_time

    @deal_time.setter
    def deal_time(self, deal_time):
        self._deal_time = deal_time

    def __str__(self):
        return "order_num: %s, order_title: %s, order_reason:%s, deal_time:%s" % (self._order_num, self._order_title,
                                                                                  self._order_reason, self._deal_time)
