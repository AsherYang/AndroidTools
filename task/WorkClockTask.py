#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/16
Desc  : 上班打卡提醒
"""
from util.SchedulerUtil import SchedulerUtil
from weather.send_msg_email import SendEmail


class WorkClockTask:
    def __init__(self):
        pass

    # work clock on work day 9:30
    def add_work_clock(self):
        scheduler = SchedulerUtil()
        scheduler.addJob(job_func=self.notifySms, id='work_cron', trigger='cron',
                         day_of_week='mon-fri', hour='9', minute='30')
        scheduler.start()

    def notifySms(self):
        sendEmail = SendEmail(toaddrs=['13714325295@139.com'], subject="小帆提醒您")
        sendEmail.send("小芬芬, 要打卡啦~")
