#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/20
Desc  : Tips 显示提醒任务
"""

from util.SchedulerUtil import SchedulerUtil


class TipsTask:
    def __init__(self):
        pass

    # tips show every 30min
    def add_tips_job(self, func, args=None):
        scheduler = SchedulerUtil()
        scheduler.setScheduler(scheduler.qtScheduler())
        scheduler.addJob(job_func=func, args=args, id='tips_cron',
                         trigger=scheduler.cronTrigger(minute='*/1'))
        scheduler.start()
