# -*- coding: UTF-8 -*-
from gtest.exceptions import *
import re


class Matcher(object):
    @staticmethod
    def match(keys, source, deal, caller):
        """
        :param keys: 每个调用者提供的支持的字段
        :param source:  要用于匹配的字段集(字典)
        :param deal:   在匹配前对字段集进入预处理
        :param caller:   调用者本身
        :return: 返回匹配好的数组，其中每项【待运行的方法， 运行优先级， 要传递给方法的参数】
        """
        exec_list = list()
        for key, value in deal(source).items():
            if key in keys:
                item = list(keys[key])
                item.append(value)
                exec_list.append(item)
            else:  # 出现不支持的字段，不报错但警告
                if key != '__line__':  # 忽略导入时自动添加的__line__字段
                    '''warn: miss 不支持的字段警告'''
                    pass
        exec_list = sorted(exec_list, key=lambda x: x[1])  # 根据字段处理优先级排序，数字越低越先执行
        return exec_list

    @staticmethod
    def if_match(keys, source, caller):
        exec_list = list()
        for key, value in source.items():
            if re.search('_[a-zA-Z0-9_]+$', key):
                key = key.split('_')[0]
            if key in keys:
                item = list(keys[key])
                item.append(value)
                exec_list.append(item)
            else:
                DataError('{} has no key named {}'.format(type(caller), key))
        exec_list = sorted(exec_list, key=lambda x: x[1])
        return exec_list

