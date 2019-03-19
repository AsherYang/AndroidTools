#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/1
Desc  : 定时任务工具类

https://zhuanlan.zhihu.com/p/46948464
"""

import logging

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from weather.send_msg_email import SendEmail

logging.basicConfig()
_logger = logging.getLogger(__name__)


class SchedulerUtil:
    def __init__(self):
        self.mysqldb = ""
        self.mysqlurl = "mysql+mysqldb://root:ouyangfan@localhost:3306/android_tools?charset=utf8"
        self.job_stores = {
            'default': SQLAlchemyJobStore(url=self.mysqlurl)
        }
        self.executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.trigger = None
        self.scheduler = self.backgroundScheduler()
        # self.scheduler = BlockingScheduler()

    """
    # self.scheduler.add_job(func=job_func, id='job_cron', trigger='cron', hour=11, minute=00,
    #                        misfire_grace_time=60, replace_existing=True)
    # self.scheduler.add_job(func=job_func, args=['job_cr', ], trigger='cron', hour=10, minute=02)
    # self.scheduler.add_job(func=job_func, trigger='interval', seconds=2)
    """
    def addJob(self, job_func, args=None, id=None, trigger=None, **trigger_args):
        self.scheduler.add_job(func=job_func, args=args, id=id, trigger=trigger, misfire_grace_time=60,
                               replace_existing=True, **trigger_args)

    def setScheduler(self, scheduler=None):
        if not scheduler:
            self.scheduler = self.backgroundScheduler()
            return
        self.scheduler = scheduler

    # BackgroundScheduler
    def backgroundScheduler(self):
        return BackgroundScheduler(jobstores=self.job_stores, excutors=self.executors,
                                   job_defaults=self.job_defaults, daemon=True)

    # BlockingScheduler
    def blockingScheduler(self):
        return BlockingScheduler(jobstores=self.job_stores, excutors=self.executors,
                                 job_defaults=self.job_defaults)

    # QtScheduler
    def qtScheduler(self):
        return QtScheduler()

    def setTrigger(self, trigger=None):
        if not trigger:
            self.trigger = CronTrigger(day_of_week='mon-fri', hour='9', minute='30')
            return
        self.trigger = trigger

    # IntervalTrigger
    def intervalTrigger(self, **kwargs):
        trigger = IntervalTrigger(**kwargs)
        return trigger

    # CronTrigger
    def cronTrigger(self, **kwargs):
        trigger = CronTrigger(**kwargs)
        return trigger

    def start(self):
        self.scheduler.start()

    # job function
    @staticmethod
    def tick():
        sendEmail = SendEmail(subject="小帆提醒您")
        sendEmail.send("小芬芬, 要打卡啦~")


if __name__ == '__main__':
    schedulerUtil = SchedulerUtil()
    schedulerUtil.addJob(job_func=SchedulerUtil.tick, id='job_interval', trigger='interval', seconds=2)
    schedulerUtil.start()
