#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/9
Desc  : adb 数据实体
"""


class TipsBean:
    def __init__(self):
        self._tips_type = None
        self._tips_desc = None

    @property
    def tips_type(self):
        return self._tips_type

    @tips_type.setter
    def tips_type(self, tips_type):
        self._tips_type = tips_type

    @property
    def tips_desc(self):
        return self._tips_desc

    @tips_desc.setter
    def tips_desc(self, tips_desc):
        self._tips_desc = tips_desc

    def __str__(self):
        return "tips_type: %s, tips_desc: %s " % (self._tips_type, self._tips_desc)
