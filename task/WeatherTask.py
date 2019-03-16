#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/16
Desc  : 天气提醒任务
"""

from util.SchedulerUtil import SchedulerUtil


class WeatherTask:
    def __init__(self):
        pass

    # weather every day 8:30, 12:30, 17:30
    def add_weather_job(self, func):
        scheduler = SchedulerUtil()
        scheduler.addJob(job_func=func, id='weather_cron', trigger='cron', hour='8,12,17', minute='30')
        scheduler.start()
