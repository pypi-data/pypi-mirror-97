#!/usr/bin/env python 
# coding=utf-8
# @Time : 2021/2/1 15:09 
# @Author : HL 
# @Site :  
# @File : Logger.py 
# @Software: PyCharm
import logging
import os
from logging import handlers

# class Logger(object):
#     level_relations = {
#         'debug': logging.DEBUG,
#         'info': logging.INFO,
#         'warning': logging.WARNING,
#         'error': logging.ERROR,
#         'crit': logging.CRITICAL
#     }  # 日志级别关系映射
#     datefmt = '%Y-%m-%d %H:%M:%S'
#
#     def __init__(self, filename, level='info', when='D', backCount=3,
#                  fmt='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s : %(message)s'):
#         self.logger = logging.getLogger(filename)
#         format_str = logging.Formatter(fmt, self.datefmt)  # 设置日志格式
#         self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
#         sh = logging.StreamHandler()  # 往屏幕上输出
#         sh.setFormatter(format_str)  # 设置屏幕上显示的格式
#         th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
#                                                encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
#         # 实例化TimedRotatingFileHandler
#         # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
#         # S 秒
#         # M 分
#         # H 小时、
#         # D 天、
#         # W 每星期（interval==0时代表星期一）
#         # midnight 每天凌晨
#         th.setFormatter(format_str)  # 设置文件里写入的格式
#         self.logger.addHandler(sh)  # 把对象加到logger里
#         self.logger.addHandler(th)
from os.path import *


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    datefmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self, path1, path2, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s : %(message)s'):
        self.logger_info = logging.getLogger(path1)
        self.logger_error = logging.getLogger(path2)
        format_str = logging.Formatter(fmt, self.datefmt)  # 设置日志格式
        self.logger_info.setLevel(self.level_relations.get(level))  # 设置日志级别
        self.logger_error.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th1 = handlers.TimedRotatingFileHandler(filename=path1, when=when, backupCount=backCount,
                                                encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th2 = handlers.TimedRotatingFileHandler(filename=path2, when=when, backupCount=backCount,
                                                encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th1.setFormatter(format_str)  # 设置文件里写入的格式
        th2.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger_info.addHandler(sh)  # 把对象加到logger里
        self.logger_info.addHandler(th1)
        self.logger_error.addHandler(sh)  # 把对象加到logger里
        self.logger_error.addHandler(th2)


# if __name__ == '__main__':
    # log = Logger('all.log', level='debug')
    # log.logger.debug('debug')
    # log.logger.info('info')
    # log.logger.warning('警告')
    # log.logger.error('报错')
    # log.logger.critical('严重')

    # abpath = dirname(abspath(__file__))
    # path1 = os.path.join(abpath, 'logs/info.log')
    # path2 = os.path.join(abpath, 'logs/error.log')
    # log = Logger(path1, path2, level='info')
    # log.logger_error.debug('debug')
    # log.logger_error.info('info')
    # log.logger_error.warning('警告')
    # log.logger_info.error('报错')
    # log.logger_error.critical('严重')
