#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : Android Tools 为一款工作中使用到的android功能工具集

为了方便日常android工作，所开发的桌面版工具。
"""

import os
import subprocess
import sys
import threading

import MySQLdb
from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QLocalServer, QLocalSocket

from constant import AppConstants
from constant import DbConstant
from util import DbUtil
from util import QSettingsUtil
from util import SupportFiles
from util.EncodeUtil import _translate, _fromUtf8
from util.RunSysCommand import RunSysCommand
from view.AdbToolView import AdbToolView
from view.BaseInfoView import BaseInfoView
from view.OtherToolsView import OtherToolsView
from view.SettingsView import SettingsView
from view.StrTransformView import StrTransformView
from view.TrayIcon import TrayIcon
from win import WinCommandEnCoding
from win.WinWTSMonitor import WinWTSMonitor

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class Ui_MainWidget(object):
    def setupUi(self, mainWindow, localServer, argv=None):
        self.mainWindow = mainWindow
        # 解决多终端问题 http://www.oschina.net/code/snippet_54100_629
        self.localServer = localServer
        self.wtsMonitor = WinWTSMonitor()
        mainWindow.setObjectName(_fromUtf8("MainWindow"))
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        # container Widget
        self.containerWidget = QtGui.QStackedWidget()
        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.menuBar = QtGui.QMenuBar(mainWindow)

        # Views
        views = self.menuBar.addMenu('&View')
        self.viewBaseInfoAction = QtGui.QAction(_fromUtf8("解析 apk"), mainWindow)
        self.viewBaseInfoAction.connect(self.viewBaseInfoAction, QtCore.SIGNAL('triggered()'), self.openBaseInfoView)
        self.viewStrTransformAction = QtGui.QAction(_fromUtf8("&字符串转换"), mainWindow)
        self.viewStrTransformAction.connect(self.viewStrTransformAction, QtCore.SIGNAL('triggered()'),
                                            self.openStrTransformView)
        views.addAction(self.viewBaseInfoAction)
        views.addAction(self.viewStrTransformAction)

        # Tools
        tools = self.menuBar.addMenu('&Tools')
        self.toolOpenCmdAction = QtGui.QAction(_fromUtf8('打开cmd终端'), mainWindow)
        self.toolOpenCmdAction.connect(self.toolOpenCmdAction, QtCore.SIGNAL('triggered()'), self.openCmdByThread)
        self.toolAdbAction = QtGui.QAction(_fromUtf8('adb 工具'), mainWindow)
        self.toolAdbAction.connect(self.toolAdbAction, QtCore.SIGNAL('triggered()'), self.openAdbToolView)
        self.toolOtherAction = QtGui.QAction(_fromUtf8('其他工具'), mainWindow)
        self.toolOtherAction.connect(self.toolOtherAction, QtCore.SIGNAL('triggered()'), self.openOtherToolsView)
        tools.addAction(self.toolOpenCmdAction)
        tools.addAction(self.toolAdbAction)
        tools.addAction(self.toolOtherAction)

        # Settings
        settings = self.menuBar.addMenu('&Setting')
        self.settingAction = QtGui.QAction(_fromUtf8("&设置"), mainWindow)
        self.settingAction.connect(self.settingAction, QtCore.SIGNAL('triggered()'), self.openSettingView)
        settings.addAction(self.settingAction)

        # 布局开始
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 2, 5, 2)

        baseInfoView = BaseInfoView()
        self.containerWidget.addWidget(baseInfoView)
        self.mainLayout.addWidget(self.containerWidget)
        self.centralwidget.setLayout(self.mainLayout)

        # 处理右键打开，或者直接拖文件到桌面图标启动。
        # argv 参数大于1，说明有其他文件路径。第0位是当前应用程序，第1位则是我们需要处理的文件路径
        # 注意这里，是需要处理sys.argv 的编码问题的，方法是使用 WinCommandEnCoding.py 处理
        if len(argv) > 1:
            filePath = argv[1]
            if SupportFiles.hasSupportFile(filePath):
                # self.appendLog(_translate('', filePath, None))
                pass
        # 监听新到来的连接(新的终端被打开)
        self.localServer.connect(localServer, QtCore.SIGNAL('newConnection()'), self.newLocalSocketConnection)

        self.trayIcon = TrayIcon()
        self.trayIcon.showMsg("have a nice day!")

        mainWindow.setMenuBar(self.menuBar)
        mainWindow.setStatusBar(self.statusBar)
        mainWindow.setCentralWidget(self.centralwidget)

    # 监听新到来的连接(新的终端被打开)
    def newLocalSocketConnection(self):
        # print 'newLocalSocketConnection'
        # 处理新启动的程序(终端)发过来的参数
        serverSocket = self.localServer.nextPendingConnection()
        if not serverSocket:
            return
        serverSocket.waitForReadyRead(1000)
        stream = QtCore.QTextStream(serverSocket)
        stream.setCodec('UTF-8')
        pathData = str(_translate('', stream.readAll(), None))
        serverSocket.close()
        # 由于客户端在发送的时候，就已经处理只发送(传递) 打开的文件路径参数，故此处不做校验处理
        # print SupportFiles.hasSupportFile(pathData)
        if pathData and SupportFiles.hasSupportFile(pathData):
            # self.appendLog(pathData)
            # print pathData
            pass

    # statusBar tip 显示
    def showStatusBarTip(self, msg):
        self.statusBar.showMessage(msg)

    # 内容窗口替换为baseInfoView 视图窗口
    def openBaseInfoView(self):
        baseInfoView = BaseInfoView()
        self.containerWidget.addWidget(baseInfoView)
        self.containerWidget.setCurrentWidget(baseInfoView)

    # 内容窗口替换为strTransformView 视图窗口
    def openStrTransformView(self):
        strTransformView = StrTransformView()
        self.containerWidget.addWidget(strTransformView)
        self.containerWidget.setCurrentWidget(strTransformView)

    def openCmdByThread(self):
        thread = threading.Thread(target=self.openCmdMethod)
        thread.setDaemon(True)
        thread.start()

    def openCmdMethod(self):
        runSyscmd = RunSysCommand()
        cmd = 'start cmd'
        result = runSyscmd.run(str(_translate("", cmd, None)))
        if result.returncode == 0:
            print u'关闭了一个终端'

    def openAdbToolView(self):
        adbToolView = AdbToolView()
        adbToolView.setStatusTip(_fromUtf8("使用adb工具时，需要USB连接上设备"))
        self.containerWidget.addWidget(adbToolView)
        self.containerWidget.setCurrentWidget(adbToolView)

    # 打开其他工具视图
    def openOtherToolsView(self):
        otherToolsView = OtherToolsView()
        otherToolsView.setWinWTSMonitor(self.wtsMonitor)
        self.containerWidget.addWidget(otherToolsView)
        self.containerWidget.setCurrentWidget(otherToolsView)

    # 打开设置视图
    def openSettingView(self):
        settingsView = SettingsView()
        self.containerWidget.addWidget(settingsView)
        self.containerWidget.setCurrentWidget(settingsView)


class AndroidToolsMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 8 * 3, screen.height() / 6 * 3)
        # self.setFixedSize(screen.width() / 8 * 3, screen.height() / 6 * 3)
        self.setWindowTitle(AppConstants.ApplicationName)
        self.setAcceptDrops(True)

    def keyPressEvent(self, event):
        # 设置 "Ctrl+Q" 快捷键，用于程序
        if event.key() == QtCore.Qt.Key_Q and event.modifiers() == QtCore.Qt.ControlModifier:
            QtGui.QApplication.quit()

    def dragEnterEvent(self, event):
        # http://www.iana.org/assignments/media-types/media-types.xhtml
        if event.mimeData().hasUrls() and event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                filePath = str(url.toLocalFile()).decode('utf-8')
                if SupportFiles.hasSupportFile(filePath):
                    event.acceptProposedAction()
                else:
                    print 'not accept this file!'
        else:
            print 'not accept this file too!'

    # 和 dragEnterEvent 结合使用，处理拖拽文件进窗口区域，进行打开。与右键和拖文件到桌面图标打开方式不同。
    # 本方式是在窗口打开的前提下，直接拖文件到窗口上，这种方式打开。
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filePath = str(url.toLocalFile()).decode('utf-8')
                # print filePath
                self.emit(QtCore.SIGNAL('dropOpenFileSignal(QString)'), filePath)
        return

    def dropOpenFileSignal(self, filePath):
        return


def main():
    app = QtGui.QApplication(sys.argv)
    androidToolsMainWin = AndroidToolsMainWindow()
    uiMainWidget = Ui_MainWidget()
    winOsArgv = WinCommandEnCoding.getOsArgv()
    # single QApplication solution
    # http://blog.csdn.net/softdzf/article/details/6704187
    serverName = 'AndroidToolsServer'
    clientSocket = QLocalSocket()
    clientSocket.connectToServer(serverName)
    QSettingsUtil.init()
    # 如果连接成功， 表明server 已经存在，当前已经有实例在运行, 将参数发送给服务端
    if clientSocket.waitForConnected(500):
        # print u'连接成功 arg = ', winOsArgv
        stream = QtCore.QTextStream(clientSocket)
        # for i in range(0, len(winOsArgv)):
        #     stream << winOsArgv[i]
        # 对于打开终端来说，所携带参数为第1位(打开文件的地址)，第0位为本执行程序地址
        if len(winOsArgv) > 1:
            stream << winOsArgv[1]
            stream.setCodec('UTF-8')
            stream.flush()
            clientSocket.waitForBytesWritten()
        # close client socket
        clientSocket.close()
        return app.quit()
    # 如果没有实例执行，创建服务器
    localServer = QLocalServer()
    # 一直监听端口
    localServer.listen(serverName)
    # create db
    createDb()
    try:
        uiMainWidget.setupUi(androidToolsMainWin, localServer, winOsArgv)
        androidToolsMainWin.show()
        sys.exit(app.exec_())
    finally:
        localServer.close()


# 需要先手动在数据库里，建立好数据仓库，才能创建表
# create DATABASE android_tools
def createDb():
    db = DbUtil.getDb()
    cursor = DbUtil.getConn(db)
    if cursor is None:
        db.close()
        return
    try:
        cursor.execute('select count(*) from adb_cmds')
        cursor.fetchall()
    except MySQLdb.ProgrammingError:
        subprocess.check_call([
            'mysql',
            '--host=' + DbConstant.dbHost,
            '--database=' + DbConstant.dbName,
            '--user=' + DbConstant.dbUser,
            '--password=' + DbConstant.dbPwd,
        ], stdin=open(os.path.join(os.path.dirname(__file__), 'constant', 'schema_androidtools.sql')))
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    main()
