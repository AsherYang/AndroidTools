#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/1/3
Desc  : 运行系统 cmd 命令
"""

import subprocess


class RunSysCommand:
    def __init__(self):
        pass

    # 这种方法直接调用，不输出结果
    # def run(self, command):
    #     return subprocess.call(command, shell=True)

    # 该种方法可以获取到终端输出结果
    # 通过 callback 把 msg 传递出去。
    # should_process=True, 默认解析数据，并通过callBack回调出去。
    def run(self, command, callback=None, should_process=True, shell=True):
        process = subprocess.Popen(command, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while should_process and process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                # print "out put = ", format(line)
                if callback:
                    callback(format(line))
        if process.returncode == 0:
            # print 'sub process success.'
            if callback:
                callback('sub process success.')
        else:
            # print 'sub process fail.'
            if callback:
                callback('sub process fail.')
        return process


if __name__ == '__main__':
    runSysCmd = RunSysCommand()
    # runSysCmd.run("start cmd", None)
    cmd = u"adb shell dumpsys power"
    runSysCmd.run(cmd, None)
