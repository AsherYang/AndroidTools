#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/18
Desc  : Android Tools 为一款工作中使用到的android功能工具集

为了方便日常android工作，所开发的桌面版工具。
"""

import sys
import threading

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtNetwork import QLocalServer, QLocalSocket

from constant import AppConstants
from util import SupportFiles
from util.EncodeUtil import _translate, _fromUtf8, _translateUtf8
from util.QtFontUtil import QtFontUtil
from util.RunSysCommand import RunSysCommand
from win import WinCommandEnCoding

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class Ui_MainWidget(object):
    def setupUi(self, mainWindow, localServer, argv=None):
        self.mainWindow = mainWindow
        # 解决多终端问题 http://www.oschina.net/code/snippet_54100_629
        self.localServer = localServer
        mainWindow.setObjectName(_fromUtf8("MainWindow"))
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.menuBar = QtGui.QMenuBar(mainWindow)

        # Tools
        tools = self.menuBar.addMenu('&Tools')
        self.toolOpenCmdAction = QtGui.QAction(_fromUtf8('打开cmd终端'), mainWindow)
        self.toolOpenCmdAction.connect(self.toolOpenCmdAction, QtCore.SIGNAL('triggered()'), self.openCmdByThread)
        tools.addAction(self.toolOpenCmdAction)

        # 布局开始
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 2, 5, 2)
        # show log
        self.logTextEdit = QtGui.QTextEdit()
        self.logTextEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logTextEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.logTextEdit.connect(self.logTextEdit, QtCore.SIGNAL('appendLogSignal(QString)'), self.appendLog)

        self.mainLayout.addWidget(self.logTextEdit)
        self.centralwidget.setLayout(self.mainLayout)

        # 处理右键打开，或者直接拖文件到桌面图标启动。
        # argv 参数大于1，说明有其他文件路径。第0位是当前应用程序，第1位则是我们需要处理的文件路径
        # 注意这里，是需要处理sys.argv 的编码问题的，方法是使用 WinCommandEnCoding.py 处理
        if len(argv) > 1:
            filePath = argv[1]
            if SupportFiles.hasSupportFile(filePath):
                self.appendLog(_translate('', filePath, None))
        # 监听新到来的连接(新的终端被打开)
        self.localServer.connect(localServer, QtCore.SIGNAL('newConnection()'), self.newLocalSocketConnection)

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
            self.appendLog(pathData)
            # print pathData

    # LOG 显示
    def appendLog(self, logTxt):
        self.logTextEdit.append(_translateUtf8(logTxt))

    # 解决在子线程中刷新UI 的问题。' QWidget::repaint: Recursive repaint detected '
    def appendLogSignal(self, logTxt):
        pass

    def emitAppendLogSignal(self, logTxt):
        self.logTextEdit.emit(QtCore.SIGNAL('appendLogSignal(QString)'), logTxt)

    # statusBar tip 显示
    def showStatusBarTip(self, msg):
        self.statusBar.showMessage(msg)

    def openCmdByThread(self):
        self.appendLog(u'正在打开cmd终端..')
        thread = threading.Thread(target=self.openCmdMethod, args=(self.emitAppendLogSignal,))
        thread.setDaemon(True)
        thread.start()

    def openCmdMethod(self, callback):
        runSyscmd = RunSysCommand()
        cmd = 'start cmd'
        result = runSyscmd.run(str(_translate("", cmd, None)))
        if result.returncode == 0:
            callback(_fromUtf8('关闭了一个终端'))


class AndroidToolsMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 8 * 3, screen.height() / 6 * 3)
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
    try:
        uiMainWidget.setupUi(androidToolsMainWin, localServer, winOsArgv)
        androidToolsMainWin.show()
        sys.exit(app.exec_())
    finally:
        localServer.close()


if __name__ == '__main__':
    main()
