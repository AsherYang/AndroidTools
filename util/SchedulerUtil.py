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
        self.scheduler = BackgroundScheduler(jobstores=self.job_stores, excutors=self.executors,
                                             job_defaults=self.job_defaults, daemon=True)
        # self.scheduler = BlockingScheduler()

    """
    # self.scheduler.add_job(func=job_func, id='job_cron', trigger='cron', hour=11, minute=00,
    #                        misfire_grace_time=60, replace_existing=True)
    # self.scheduler.add_job(func=job_func, args=['job_cr', ], trigger='cron', hour=10, minute=02)
    # self.scheduler.add_job(func=job_func, trigger='interval', seconds=2)
    """
    def addJob(self, job_func, id=None, trigger=None, **trigger_args):
        self.scheduler.add_job(func=job_func, id=id, trigger=trigger, misfire_grace_time=60,
                               replace_existing=True, **trigger_args)

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
