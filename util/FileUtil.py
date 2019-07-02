#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/22
Desc  : 文件操作类
http://blog.csdn.net/ziyuzhao123/article/details/8811496
"""

import os
import shutil


# 从文件路径中提取文件名(包括后缀拓展名)
def getFileName(filePath):
    fileName = 'UnKnownFile'
    if not filePath:
        return fileName
    filePath = unicode(filePath)
    return os.path.basename(filePath)


# 返回文件拓展名(不包含点".")
def getFileExt(filePath):
    fileExt = 'UnknownFileExt'
    if not filePath:
        return fileExt
    filePath = unicode(filePath)
    return os.path.splitext(filePath)[1][1:].lower()


# 返回文件名(包括文件目录, 但不包含扩展名)
def getFilePathWithName(filePath):
    if not filePath:
        return './'
    filePath = unicode(filePath)
    return os.path.splitext(filePath)[0]


# 返回文件父目录
def getFileDir(filePath):
    if not filePath:
        return './'
    filePath = unicode(filePath)
    return os.path.dirname(filePath)


# 获取指定目录及其子目录下, 所有文件
def getAllFiles(dir):
    dir = unicode(dir)
    fileList = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            fileList.append(os.path.join(root, file))
    return fileList


# 获取指定目录及其子目录下，指定文件名的文件
def getAllFilesByExt(dir, fileExt):
    fileList = []
    dir = unicode(dir)
    fileExt = unicode(fileExt)
    if not fileExt:
        return fileList
    for root, dirs, files in os.walk(dir):
        for file in files:
            if fileExt == getFileExt(file):
                fileList.append(os.path.join(root, file))
    return fileList


# 获取指定目录下的子一级目录
def getSubDir(dir):
    dir = unicode(dir)
    dirList = []
    for path in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, path)):
            dirList.append(os.path.join(dir, path))
    return dirList


# 当文件目录不存在时，创建一个文件目录(创建多层目录)
def mkdirNotExist(directory):
    # 防止创建文件目录时乱码
    directory = directory.decode('utf-8')
    if not os.path.exists(directory):
        os.makedirs(directory)


# 判断文件或文件夹是否存在
def isFileOrDirExist(filePath):
    return os.path.exists(filePath)


# 拷贝文件/文件夹
def copyFile(srcDir, destDir, startSrcDir, copyFileName):
    if copyFileName:
        srcFile = os.path.join(srcDir, copyFileName)
    else:
        srcFile = srcDir
    # print '-->srcFile:%s, destFile:%s, copyFile:%s' % (srcFile, destFile, copyFileName)
    # print '--is--',os.path.isdir(srcFile)
    if os.path.isdir(srcFile):
        for root, dirs, files in os.walk(srcFile):
            for dirTmp in dirs:
                # print 'root: %s, dirs:%s, files:%s ' % (root, dirTmp, files)
                copyFile(os.path.join(root, dirTmp), destDir, startSrcDir, None)
            for fileTmp in files:
                copyFile(root, destDir, startSrcDir, fileTmp)
    else:
        destPath = srcFile.replace(startSrcDir, "")
        if destPath.startswith("/") or destPath.startswith("\\"):
            destPath = destPath[1:]
            destPath = destPath.replace("/", "\\")
        destFile = os.path.join(destDir, destPath)
        fpath, fname = os.path.split(destFile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        # print '-->222 srcFile: %s, destFile:%s' %(srcFile, destFile)
        shutil.copyfile(srcFile, destFile)


# 删除文件夹
def removeDirs(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


if __name__ == '__main__':
    copyFile("G:\\android_studio\\settings.jar", "G:\\copyfile\\2.txt")
