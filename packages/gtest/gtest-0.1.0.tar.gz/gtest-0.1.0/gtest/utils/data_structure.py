# -*- coding: UTF-8 -*-
from gtest.exceptions import *


class ListItem(object):
    def __init__(self):
        self._list = list()
    '''
    def get(self, source):
        for r in (item.get(source) for item in self._list):
            if r is not None:
                return r
        raise DataError('{} has not attr named{}'.format(type(self), source))
    '''


class Node(object):

    def __init__(self, name, parent=None, child=None):
        self.name = name
        self.parent = parent
        self.child = list(child) if child is not None else []

    def add(self, name, value):
        self.__dict__[name] = value

    def get(self, t, *args):
        return self.parent.get(t, *args)

    def set(self, *args):
        raise FrameWorkError()

    def get_parent_name(self):
        if self.parent:
            return self.parent.get_parent_name() + '\\' + self.name
        else:
            return self.name



