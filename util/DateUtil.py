#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
Author: AsherYang
Email:  ouyangfan1991@gmail.com
Date:   2018/6/15
Desc:   时间工具类
"""

import datetime
import time

class DateUtil:

    def __init__(self):
        pass

    def getCurrentTime(self):
        return datetime.datetime.now()

    # 管理员校验时效，超时使用的是时间戳形式
    def getCurrentTimeStamp(self):
        return int(time.time())

    # 将时间戳转换为格式化的日期
    def convert2Time(self, timeStamp, format_time="%Y-%m-%d %H:%M:%S"):
        time_local = time.localtime(float(timeStamp))
        format_time = time.strftime(format_time, time_local)
        return format_time

    # 将格式化日期转换为时间戳
    def convert2TimeStamp(self, time_f, format_time="%Y-%m-%d %H:%M:%S"):
        timeArray = time.strptime(str(time_f), format_time)
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

if __name__ == '__main__':
    dateUtil = DateUtil()
    print dateUtil.getCurrentTime()
    print dateUtil.getCurrentTimeStamp()
    print dateUtil.convert2Time(1553517739)
    print dateUtil.convert2TimeStamp("2019-03-25 20:42:19")
