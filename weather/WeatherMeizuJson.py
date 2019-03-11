#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/1/9
Desc  : meizu weather return json object
https://github.com/jokermonn/-Api/blob/master/MXWeather.md
http://aider.meizu.com/app/weather/listWeather?cityIds=101281601
"""
import json
from json.decoder import WHITESPACE


# 魅族接口返回总的 json 数据
class MeiZuWeatherValue:
    @property
    def city(self):
        return self.city

    @property
    def weatherDetailsInfo(self):
        return self.weatherDetailsInfo

    @property
    def weathers(self):
        return self.weathers


# 对应 weatherDetailsInfo 子字段
class WeatherDetailsInfo:
    @property
    def publishTime(self):
        return self.publishTime

    @property
    def weather3HoursDetailsInfos(self):
        return self.weather3HoursDetailsInfos


# 对应 Weathers 子字段
class Weathers:
    @property
    def date(self):
        return self.date

    @property
    def img(self):
        return self.img

    @property
    def sun_down_time(self):
        return self.sun_down_time

    @property
    def sun_rise_time(self):
        return self.sun_rise_time

    @property
    def temp_day_c(self):
        return self.temp_day_c

    @property
    def temp_night_c(self):
        return self.temp_night_c

    @property
    def wd(self):
        return self.wd

    @property
    def weather(self):
        return self.weather

    @property
    def week(self):
        return self.week

    @property
    def ws(self):
        return self.ws


# 对应 Weather3HoursDetailsInfos 子字段
class Weather3HoursDetailsInfos:
    @property
    def endTime(self):
        return self.endTime

    @property
    def highestTemperature(self):
        return self.highestTemperature

    @property
    def img(self):
        return self.img

    @property
    def isRainFall(self):
        return self.isRainFall

    @property
    def lowerestTemperature(self):
        return self.lowerestTemperature

    @property
    def precipitation(self):
        return self.precipitation

    @property
    def startTime(self):
        return self.startTime

    @property
    def wd(self):
        return self.wd

    @property
    def weather(self):
        return self.weather

    @property
    def ws(self):
        return self.ws


# json decode
class WeatherDecode(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        dic = super(WeatherDecode, self).decode(s)
        print dic
        weatherValue = MeiZuWeatherValue()
        weatherDetailsInfo = WeatherDetailsInfo()
        weathers = Weathers()
        weather3HoursDetailsInfos = Weather3HoursDetailsInfos()

        weatherList0 = dic['value'][0]
        weatherValue.city = weatherList0['city']

        weathersList0 = weatherList0['weathers'][0]
        weathers.date = weathersList0['date']
        weathers.img = weathersList0['img']
        weathers.sun_down_time = weathersList0['sun_down_time']
        weathers.sun_rise_time = weathersList0['sun_rise_time']
        weathers.temp_day_c = weathersList0['temp_day_c']
        weathers.temp_night_c = weathersList0['temp_night_c']
        weathers.wd = weathersList0['wd']
        weathers.weather = weathersList0['weather']
        weathers.week = weathersList0['week']
        weathers.ws = weathersList0['ws']

        weather3HoursDetailsInfosList0 = weatherList0['weatherDetailsInfo']['weather3HoursDetailsInfos'][0]
        weather3HoursDetailsInfos.endTime = weather3HoursDetailsInfosList0['endTime']
        weather3HoursDetailsInfos.highestTemperature = weather3HoursDetailsInfosList0['highestTemperature']
        weather3HoursDetailsInfos.img = weather3HoursDetailsInfosList0['img']
        weather3HoursDetailsInfos.isRainFall = weather3HoursDetailsInfosList0['isRainFall']
        weather3HoursDetailsInfos.lowerestTemperature = weather3HoursDetailsInfosList0['lowerestTemperature']
        weather3HoursDetailsInfos.precipitation = weather3HoursDetailsInfosList0['precipitation']
        weather3HoursDetailsInfos.startTime = weather3HoursDetailsInfosList0['startTime']
        weather3HoursDetailsInfos.wd = weather3HoursDetailsInfosList0['wd']
        weather3HoursDetailsInfos.weather = weather3HoursDetailsInfosList0['weather']
        weather3HoursDetailsInfos.ws = weather3HoursDetailsInfosList0['ws']

        weatherDetailsInfo.publishTime = weatherList0['weatherDetailsInfo']['publishTime']
        weatherDetailsInfo.weather3HoursDetailsInfos = weather3HoursDetailsInfos
        weatherValue.weatherDetailsInfo = weatherDetailsInfo
        weatherValue.weathers = weathers
        return weatherValue

