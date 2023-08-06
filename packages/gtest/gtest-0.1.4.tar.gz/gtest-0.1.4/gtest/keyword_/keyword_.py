# -*- coding: UTF-8 -*-
from gtest.keyword_.selenium_ import keyword as sk
from gtest.model.matcher.var_matcher import VarMatcher as M
from gtest.keyword_.Random import keyword as rk
from gtest.keyword_.common import keyword as ck
from gtest.exceptions import *
from gtest.utils.data_structure import Node
KEYWORD = rk
KEYWORD.update(sk)
KEYWORD.update(ck)


class KeyWord(Node):

    def __init__(self, key, args, return_var, parent):
        if not self.has_key(key):
            raise DataError('keyword:{} don\'t exist'.format(key))
        Node.__init__(self, key, parent)
        self.func = KEYWORD[key]
        self.inner_args, self.args, self.return_var = [list() for i in range(0, 3)]
        self.keyword_args = dict()
        self.analyze_var(self.func)
        "miss: 组织好keyword的格式"
        self.source = str(key) + str(args) + str(return_var)

        la, lb = M.keyword_args_match(args)
        if len(self.args) != len(la) and not self.check_variable(self.args):
            raise DataError('Keyword {} required {} but given {}'.format(key, len(self.args), len(la)))
        for i in range(0, len(la)):
            t = M.args_match(la[i])
            if t is not None:
                data = self.get('vars', *t)
                self.args[i]['value'] = M.inner_args_match(data['value'], self)
                self.args[i]['value_description'] = data['description']
            else:
                self.args[i]['value'] = M.inner_args_match(la[i], self)
        for key, value in lb.items():
            self.keyword_args[key]['value'] = M.inner_args_match(value, self)
        if return_var is not None and len(return_var) != 0:
            self.set(*return_var)

    def analyze_var(self, f):
        if f.__doc__ is None:
            return
        vars = [i.replace(':', '').split() for i in f.__doc__.split('\n')[1:-1]]
        for var in vars:
            if var[0] == 'param':
                self.args.append({'name': var[1], 'description': var[2], 'value': None})
            elif var[0] == 'inner_param':
                self.inner_args.append({'name': var[1], 'description': var[2], 'value': None})
            elif var[0] == 'keyword_param':
                self.keyword_args[var[1]] = ({'description': var[2], 'value': None})
            elif var[0] == 'return':
                for i in range(1, len(var), 2):
                    self.return_var.append({'name': var[i], 'description': var[i+1]})

    def set(self, *args):
        self.parent.set(*args)

    @staticmethod
    def has_key(key):
        if key in KEYWORD:
            return True
        return False

    @staticmethod
    def check_variable(args):
        for arg in args:
            if '*' in arg['name']:
                return True
        return False

"""
    ###### test_code ############################################################################
"""


class _mock(object):
    def set(self, *args):
        for item in args:
            print('#set {}'.format(item))

    def get(self, t, *args):
        return {'value': '#value#', 'description': '#desc#', 'group': '#group#'}


if __name__ == '__main__':
    l = ['a', 'b', 'cc', '*sad']
    print(KeyWord.check_variable(l))