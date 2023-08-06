# -*- coding: UTF-8 -*-
import time


class Logger(object):
    """全局logger"""
    '''log_level日志等级'''
    ERROR = 'ERROR'
    WARN = ' WARN'
    DEBUG = 'DEBUG'
    INFO = ' INFO'
    '''详细程度'''
    prefix = ''

    def __init__(self):
        self.cache = list()
        self.prefix = ''

    def error(self, msg):
        self.cache.append(Log(msg, Logger.ERROR, self.prefix))

    def warn(self, msg):
        self.cache.append(Log(msg, Logger.WARN, self.prefix))

    def debug(self, msg):
        self.cache.append(Log(msg, Logger.DEBUG, self.prefix))

    def info(self, msg):
        self.cache.append(Log(msg, Logger.INFO, self.prefix))

    def reset_prefix(self):
        self.prefix = ''

    def add_prefix(self):
        self.prefix += '》》'

    def sub_prefix(self):
        self.prefix = self.prefix.replace('》》', '', 1)


class Log(object):
    def __init__(self, msg, level, prefix):
        self.time = self._get_time()
        self.level = level
        self.msg = msg
        if type(msg) == list:
            for m in msg:
                print('{}:{}:{}{}'.format(self.time, self.level, prefix, m))
        else:
            print('{}:{}:{}{}'.format(self.time, self.level, prefix, msg))

    def _get_time(self):
        return time.strftime("%H:%M:%S", time.localtime())


logger = Logger()
