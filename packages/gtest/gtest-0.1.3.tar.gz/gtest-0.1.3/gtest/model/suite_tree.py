# -*- coding: UTF-8 -*-
from gtest.utils.data_structure import Node
from gtest.utils.common import check, search_line, lower
from gtest.exceptions import *
from gtest.model.matcher.matcher import Matcher
from gtest.model.groups import Groups
from gtest.model.cases import Case, Step, Template
from gtest.model.suite_file_tree import SuiteFile


class Suite(Node):

    def __init__(self, name, source, path, _type, parent):
        Node.__init__(self, name, parent=parent)
        self.cases, self.setup, self.teardown, self.case_setup, \
        self.case_teardown, self.vars, self.templates, self.tag = [None for i in range(0, 8)]
        self.type = _type  # 沿用FileTree的类型，1=DIR， 2=File
        self.source_path = path
        if source is not None:
            self.source = lower(source)  # 将字段改小写
            self._check(self.source)
            exec_list = Matcher.match(self.Key, self.source, self._deal, self)  # 匹配字段
            for e in exec_list:
                e[0](self, e[2])  # 执行 miss: eval(e[0], [self, e[2]])
        else:  # 文件夹下没有suite.yml时path为None
            self.source = None
            self.path = None

    def get(self, t, *args):
        """
        :param t:  要查找的类型：vars变量，template模板，setup/teardown前后置步骤
        :param args:  查找的关键词
        :return:  返回查找的数据，找不到则raise exception
        """
        if not hasattr(self, t):
            raise FrameWorkError(t, *args)
        if t == 'vars':
            result = self.vars.get(*args) if self.vars else None
        elif t == 'templates':
            result = self.templates[args[0]] if self.templates and args[0] in self.templates else None
        else:
            result = getattr(self, t)
        if result:
            return result
        if self.parent:
            return self.parent.get(t, *args)
        else:
            '''miss：line'''
            raise DataError('miss')

    def set(self, t, *args):
        """设置动态变量"""
        self.vars.set(t, *args)

    def clear(self, t):
        """清除上个template或case留下的动态变量"""
        if self.vars:
            self.vars.clear(t)

    def _deal(self, source):
        """解析数据前的预处理函数"""
        if self.type == SuiteFile.DIR and 'case' in source:  # suite.yml文件不能有case字段
            raise UseAttrError('suite.yml文件', 'case', search_line(source))
        elif self.type == SuiteFile.FILE and 'case' not in source:
            raise MissAttrError('Suite', 'case', '记录测试用例', 0)
        elif 'var' not in source:
            self.vars = Groups(None, self) if not self.vars else self.vars  # 如果vars为None则还是要初始化group用于支持动态变量
        return source

    def _parse_variables(self, source):
        if source is None:  # 允许字段为空，只警告
            '''warn: miss var字段为空'''
            return
        source = check(source, ('Suite', 'var'))  # 检查source的类型，并处理
        self.vars = Groups(source, self)

    def _parse_settings(self, source):
        pass

    def _parse_template(self, source):
        if source is None:  # 允许template字段为空，只警告
            '''warn: miss template字段为空'''
            return
        source = check(source, ('Suite', 'template'))  # 检查source的类型，并处理
        self.templates = dict()
        for temp in source:
            t = Template(lower(temp), self)
            self.templates[t.name] = t

    def _parse_pre_and_post(self, name, source):
        if source is None:  # 允许字段为空，只警告
            '''warn: miss'''
            pass
        source = check(source, ('Suite', name))  # 检查source的类型，并处理
        setattr(self, name, [Step(lower(step), self) for step in source])

    def _parse_cases(self, source):
        if source is None:
            raise NoneAttrError('Suite', 'case', search_line(source))
        source = check(source, ('Suite', 'case'))
        self.cases = [Case(case, self) for case in source]

    def _parse_tag(self, tags):
        if tags:
            '''warn: miss'''
        s_type = type(tags)
        if s_type == list:
            self.tag = tags
        elif s_type == str:
            self.tag = [tags]
        else:
            '''warn: miss'''

    def _check(self, source):
        if source is None:
            raise MissAttrError('Suite', 'case', '记录测试用例', 0)
        elif type(source) == dict:
            pass
        else:
            raise AttrTypeError('Suite', '根目录下', '键值对', 0)

        '''支持的字段         对应方法        执行顺序(正序)'''
    Key = {
            'var':        [(lambda caller, x: caller._parse_variables(x)),      1],
            'setting':         [(lambda caller, x: caller._parse_settings(x)),       0],
            'case':            [(lambda caller, x: caller._parse_cases(x)),         99],
            'setup':            [(lambda caller, x: caller._parse_pre_and_post('setup', x)),         11],
            'teardown':         [(lambda caller, x: caller._parse_pre_and_post('teardown', x)),      12],
            'case_setup':       [(lambda caller, x: caller._parse_pre_and_post('case_setup', x)),    13],
            'case_teardown':    [(lambda caller, x: caller._parse_pre_and_post('case_teardown', x)), 14],
            'tag':              [(lambda caller, x: caller._parse_tag(x)),            5],
            'templates':        [(lambda caller, x: caller._parse_template(x)), 2]
    }


class SuiteTree(object):
    def __init__(self, source_tree, options):
        self.parent = None
        self.root = self.parse_suite(source_tree.root, None)

    def parse_suite(self, source_root, parent):
        '''
        :description: 递归解析每个目录下suite文件
        :param root: 当前的Suite节点
        :param source_root:  当前的SuiteFile节点
        :param parent:  当前的Suite节点的父节点
        :return:  root
        '''
        root = Suite(source_root.name, source_root.source, source_root.source_path, source_root.type, parent)
        len_child = len(source_root.child)
        if len_child == 0:
            return root
        for i in range(len_child):
            root.child.append(self.parse_suite(source_root.child[i-1], root))
        return root


"""
    ###### test_code ############################################################################
"""
if __name__ == '__main__':
    # with open(os.path.join('../../data', 'test', 'test.yml'), 'rb') as f:
    #     data = yaml.load(f)
    print([None for i in range(1, 6)])
