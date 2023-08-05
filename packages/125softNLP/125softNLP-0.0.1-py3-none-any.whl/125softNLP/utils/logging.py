# -*- coding: utf-8 -*-
# @Time    : 2020/11/19-16:53
# @Author  : 贾志凯    15716539228@163.com
# @File    : logging.py
# @Software: win10  python3.6 PyCharm
import sys
class logger(object):
    def __init__(self,filename):
        self.terminal = sys.stdout
        self.log = open(filename,"a")
    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
# sys.stdout = logger('logging.txt')