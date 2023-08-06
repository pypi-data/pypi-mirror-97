# -*- coding: UTF-8 -*-
from gtest.exceptions import *
import sys


def check(source, name):
    s_type = type(source)
    if s_type == dict:
        _source = [source]
    elif s_type == list:
        _source = source
    else:
        raise AttrTypeError(name[0], name[1], '键值对或者数组', search_line(source))
    return _source


def search_line(source, *keyword):
    '''
    if source is None:
        raise FrameWorkError('传到search_line的source为空')
    else:
        result = list()
        t = type(source)
        if t == list:
            _search_list(source)
        elif t == dict:
            _search_dict(source)
        result.sort()
    return result[-1]
    '''
    return 0

'''
def _search_list(source):
    for item in source:
        t = type(item)
        if t == list:
            _search_list(item)
        elif t == dict:
            _search_dict(item)
        elif t == int or t == str:
            pass

def _search_dict(source):
    pass
'''
def lower(source):
    return {str.lower(k): v for k, v in source.items()}

