# -*- coding: UTF-8 -*-
from gtest.utils.data_structure import Node
from gtest.exceptions import *
from gtest.utils.common import lower
from gtest.model.matcher.matcher import Matcher
from gtest.keyword_.keyword_ import KeyWord


class Case(Node):
    def __init__(self, source, suite):
        Node.__init__(self, None, parent=suite)
        self.step = list()
        self.setup, self.teardown, self.tag = [None, None, None]
        self.source = lower(source)

        exec_list = Matcher.match(self.Key, self.source, self._deal, self)
        for e in exec_list:
            e[0](self, e[2])
        '''获取suite级别的case setup/teardown'''
        try:
            self.setup = self.parent.get('case_setup') if self.setup is None else self.setup
        except DataError:
            pass  # 若parent都没有指定case setup/teardown，则忽略
        try:
            self.teardown = self.parent.get('case_teardown') if self.teardown is None else self.teardown
        except DataError:
            pass
        '''清除动态变量缓存'''
        self.parent.clear('case')

    def _deal(self, source):
        if 'name' not in source or 'step' not in source:
            raise DataError('case must has a {}'.format('name/step'))
        return source

    def parse_step(self, source):
        if type(source) != list:
            raise DataError('step must be list')
        for step in source:
            if 'use_template' in step:
                Step(step, self)
            else:
                self.step.append(Step(step, self))

    def set(self, *args):
        self.parent.set('case', *args)

    def parse_tags(self, tags):
        s_type = type(tags)
        if s_type == list or s_type == str:
            self.tag = tags
        else:
            if tags:
                '''warn: miss'''
            else:
                '''warn: miss'''

    def parse_setup(self, source):
        self.setup = [Step(step, self) for step in source]

    def parse_teardown(self, source):
        self.teardown = [Step(step, self) for step in source]

    '''支持的字段         对应需要调用的处理方法        执行顺序(正序)'''
    Key = {
            'name':  [(lambda caller, x: caller.add('name', x)),      0],
            'desc':       [(lambda caller, x: caller.add('description', x)),     1],
            'step':        [(lambda caller, x: caller.parse_step(x)),      4],
            'tag':          [(lambda caller, x: caller.parse_tags(x)),       11],
            'setup':  [(lambda caller, x:caller.parse_setup(x)), 2],
            'teardown': [(lambda caller, x:caller.parse_teardown(x)), 3]
    }


class Template(Node):
    def __init__(self, source, suite):
        Node.__init__(self, None, parent=suite)
        self.return_var, self.args, self.step = [None for i in range(0, 3)]
        self.source = lower(source)
        exec_list = Matcher.match(self.Key, self.source, self._deal, self)
        for e in exec_list:
            e[0](self, e[2])
        self.parent.clear('template')

    def parse_args(self, args):
        if type(args) == dict:
            self.set(args['name'])
        if type(args) == list:
            self.set(*[arg['name'] for arg in args])
        self.args = args if type(args) == list else list(args)

    def set(self, *args):
        self.parent.set('template', *args)

    def parse_return(self, return_var):
        if type(return_var) != list:
            self.return_var = [return_var]
        else:
            self.return_var = return_var

    def parse_step(self, source):
        self.step = source

    def _deal(self, source):
        if 'name' not in source:
            raise DataError('template must has a name')
        if 'step' not in source:
            raise DataError('template must has steps')
        return source

    Key = {
            'name': [(lambda caller, x: caller.add('name', x)), 0],
            'desc': [(lambda caller, x: caller.add('description', x)), 1],
            'step': [(lambda caller, x: caller.parse_step(x)), 99],
            'arg': [(lambda caller, x: caller.parse_args(x)), 2],
            'return': [(lambda caller, x: caller.parse_return(x)), 3]
    }


class Step(Node):
    def __init__(self, source, case, name=None):
        Node.__init__(self, name, parent=case)
        self.type, self.args, self.return_var, self.keyword = [None, None, None, None]
        self.source = lower(source)
        exec_list = Matcher.match(self.Key, lower(source), self._deal, self)
        for e in exec_list:
            e[0](self, e[2])

    def _deal(self, source):
        '''miss 必要字段的处理'''
        return source

    def parse_template(self, source):
        '''get template object'''
        temp = self.parent.get('templates', source)
        '''check args'''
        replace = dict()
        required = len(temp.args) if temp.args is not None else 0
        given = len(self.args) if self.args is not None else 0
        if given != required:
                raise DataError('template {} required {} args but given {}'.format(temp.name, required, given))
        if given != 0:
            for i in range(0, given):
                replace[temp.args[i]['name']] = self.args[i]
        '''check return var'''
        required = len(temp.return_var) if temp.return_var is not None else 0
        given = len(self.return_var) if self.return_var is not None else 0
        if given > required:
                raise DataError('template {} return {} args but given {} '.format(temp.name, required, given))
        '''replace args'''
        if given != 0:
            for step in temp.step:
                if 'arg' in step and step['arg'] is not None:
                    for i in range(0, len(step['arg'])):
                        arg = step['arg'][i].strip('${}')
                        step['arg'][i] = replace[arg] if arg in replace else step['arg'][i]
        '''goback to case to parse step from template'''
        self.parent.parse_step(temp.step)
        '''set return var'''
        if self.return_var:
            self.set(*self.return_var)

    def parse_keyword(self, key):
        self.type = 'keyword'
        self.keyword = KeyWord(key, self.args, self.return_var, self)

    def parse_assert(self, key):
        self.type = 'assert'
        self.keyword = KeyWord(key, self.args, self.return_var, self)

    def parse_if(self):
        self.type = 'if'
        self._if = If(self.source, self)

    def parse_args(self, args):
        if type(args) != list:
            self.args = [args]
        else:
            self.args = args

    def parse_return(self, args):
        if type(args) != list:
            self.return_var = [args]
        else:
            self.return_var: args

    def set(self, *args):
        self.parent.set('case', *args)

    '''支持的字段         对应方法        执行顺序(正序)'''
    Key = {
            'use_template':  [(lambda caller, x: caller.parse_template(x)),      11],
            'keyword':       [(lambda caller, x: caller.parse_keyword(x)),     12],
            'assert':        [(lambda caller, x: caller.parse_assert(x)),      13],
            'arg':          [(lambda caller, x: caller.parse_args(x)),        1],
            'return':        [(lambda caller, x: caller.parse_return(x)),     2],
            'desc':          [(lambda caller, x: caller.add('description', x)),              14],
            'if':            [(lambda caller, x: caller.parse_if()), 10]
    }


class If(Node):
    def __init__(self, source, case, name=None):
        Node.__init__(self, name, parent=case)
        self.condition = [None]
        self.execute = [None, None]
        self.index = 1
        self.source = lower(source)
        exec_list = Matcher.if_match(self.Key, self.source, self)
        for e in exec_list:
            e[0](self, e[2])

    def parse_if(self, source):
        if 'then' in source:
            data = source.pop('then')
            self.execute[0] = [Step(step, self) for step in data]
        self.condition[0] = Step(source, self)

    def parse_elif(self, source):
        if 'then' in source:
            data = source.pop('then')
            self.execute.insert(-1, [Step(step, self) for step in data])
        self.condition.insert(-1, [Step(step, self) for step in source])

    def parse_else(self, source):
        self.execute[-1] = [Step(step, self) for step in source]

    def set(self, *args):
        self.parent.set('case', *args)

    '''支持的字段         对应方法        执行顺序(正序)'''
    Key = {
            'if':  [(lambda caller, x: caller.parse_if(x)),      10],
            'elif':       [(lambda caller, x: caller.parse_elif(x)),     11],
            'else':        [(lambda caller, x: caller.parse_else(x)),      12],
            'then':      []
    }


"""
    test_code
"""


class Mock(object):
    def set(self, *args):
        for item in args:
            print('#set {}'.format(item))

    def get(self, t, *args):
         return {'value': '#value#', 'description': '#desc#', 'group': '#group#'}


if __name__ == '__main__':
    import yaml
    with open('../../data/gitee/test.yml', 'rb') as f:
        data = yaml.load(f, Loader=yaml.Loader)
        i = If(data, Mock)
    print()
