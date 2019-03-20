#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/3/13
Desc  : 桌面小部件
"""
import sys

from PyQt4 import QtCore, QtGui

import threading
from random import choice
from util.EncodeUtil import _fromUtf8
from util.QtFontUtil import QtFontUtil
from weather.get_weather import Weather
from task.WeatherTask import WeatherTask
from task.TipsTask import TipsTask
from db.TipsDao import TipsDao


class DesktopWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.rightButton = False
        self.dragPos = 0
        self.tipsList = []
        self.initUI()

    def initUI(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() / 20 * 16, screen.height() / 20 * 1, 350, 30)
        # we can resize the widget. https://blog.csdn.net/y673582465/article/details/73603265
        sizeGrip = QtGui.QSizeGrip(self)
        self.setWindowTitle('AndroidTools')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        quitAction = QtGui.QAction(_fromUtf8("退出"), self)
        quitAction.connect(quitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(quitAction)

        mainLayout = QtGui.QVBoxLayout()
        self.weatherlabel = QtGui.QLabel(_fromUtf8("天气"))
        self.tipsLabel = QtGui.QLabel(_fromUtf8("桌面提示"))
        self.weatherlabel.setPalette(QtFontUtil().setFontColor2Palette(QtCore.Qt.black))
        self.tipsLabel.setPalette(QtFontUtil().setFontColor2Palette(QtCore.Qt.red))
        self.weatherlabel.connect(self.weatherlabel, QtCore.SIGNAL('weatherUpdateSignal(QString)'), self.showWeather)
        self.tipsLabel.connect(self.tipsLabel, QtCore.SIGNAL('tipsChangeSignal(QString)'), self.showTips)
        mainLayout.addWidget(self.weatherlabel)
        mainLayout.addWidget(self.tipsLabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
        tranColor = QtGui.QColor(0xDE, 0xDE, 0xDE)
        self.setTransparency(tranColor)
        self.queryTipsMethod()

    def getWeather(self):
        city = '东莞'
        weather = Weather(city)
        meizuWeather = weather.getWeatherByMeizu()
        weather_now = meizuWeather.city + ": " + meizuWeather.weathers.date.replace('-', '') + \
                      meizuWeather.weathers.week + ' ' + meizuWeather.weathers.weather + \
                      meizuWeather.weathers.temp_day_c + '/' + \
                      meizuWeather.weathers.temp_night_c + u'℃'
        return weather_now

    def showWeather(self, weather_now):
        self.weatherlabel.setText(weather_now)

    def emitWeatherUpdateSignal(self):
        self.weatherlabel.emit(QtCore.SIGNAL('weatherUpdateSignal(QString)'), _fromUtf8(self.getWeather()))

    def weatherUpdateSignal(self, weather_now):
        pass

    def addWeatherJob(self):
        weatherTask = WeatherTask()
        weatherTask.add_weather_job(self.emitWeatherUpdateSignal)

    def addTipsJoB(self):
        tipsTask = TipsTask()
        tipsTask.add_tips_job(self.changeTipsShow)

    def queryTipsMethod(self):
        thread = threading.Thread(target=self.queryTipsFromDb)
        thread.setDaemon(True)
        thread.start()

    def queryTipsFromDb(self):
        tipsDao = TipsDao()
        tipsBeanList = tipsDao.queryAll()
        if not tipsBeanList:
            return
        # 重新初始化
        self.tipsList[:] = []
        for tip in tipsBeanList:
            self.tipsList.append(tip.tips_desc)
        tips = choice(self.tipsList)
        self.emitTipsChangeShow(_fromUtf8(tips))

    # 定时器中直接拿内存数据，不进行数据库查询
    def changeTipsShow(self):
        if self.tipsList:
            tips = choice(self.tipsList)
            self.emitTipsChangeShow(_fromUtf8(tips))

    def showTips(self, tips):
        self.tipsLabel.setText(unicode(tips))

    def emitTipsChangeShow(self, tips):
        self.tipsLabel.emit(QtCore.SIGNAL('tipsChangeSignal(QString)'), tips)

    def tipsChangeSignal(self, tips):
        pass

    def mouseReleaseEvent(self, event):
        if self.rightButton:
            self.rightButton = False
            self.popMenu.popup(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        if event.button() == QtCore.Qt.RightButton and not self.rightButton:
            self.rightButton = True

    # https://blog.csdn.net/seanyxie/article/details/5930779
    def setTransparency(self, color, p_float=0.5):
        p = self.palette()
        p.setColor(QtGui.QPalette.Background, color)
        self.setPalette(p)
        self.setWindowOpacity(p_float)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    desktopWidget = DesktopWidget()
    desktopWidget.show()
    sys.exit(app.exec_())
