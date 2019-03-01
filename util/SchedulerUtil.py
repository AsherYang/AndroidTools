#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/1
Desc  : 定时任务工具类

https://zhuanlan.zhihu.com/p/46948464
"""

from util.DateUtil import DateUtil
from apscheduler.schedulers.blocking import BlockingScheduler


class SchedulerUtil:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def tick(self):
        strTmp = 'Tick !  The time is: %s ' % DateUtil().getCurrentTime()
        print strTmp

    def addJob(self, job):
        self.scheduler.add_job(self.tick, 'cron', hour=10, minute=40)

    def start(self):
        self.scheduler.start()


if __name__ == '__main__':
    schedulerUtil = SchedulerUtil()
    schedulerUtil.addJob(schedulerUtil.tick())
    schedulerUtil.start()
