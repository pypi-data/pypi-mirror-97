# -*- coding: UTF-8 -*-
from gtest.utils.data_structure import Node
from gtest.utils.file import load
from gtest.exceptions import *
from gtest.utils.logger import logger
import os


class SuiteFile(Node):
    FILE = 0
    DIR = 1

    def __init__(self, name, _type, suite_file=None, parent=None, child=None):
        Node.__init__(self, name, parent, child)
        self.type = _type
        self.source_path = suite_file
        self.source = load(self.source_path) if suite_file else None
        '''为筛选做准备'''
        self.tag = self.load_tag(self.source)  # 加载标签
        self.cases = self._load_case(self.source)  # 加载用例

    def _load_case(self, source):
        """返回每个suite中的case列表"""
        if not source or 'cases' not in source:
            return None
        cases = list()
        for case in source['cases']:
            if 'name' in case:
                cases.append({'name': case['name'],
                              'tag': self.load_tag(case)})
        return cases

    def load_tag(self, source):
        """返回suite或case中的tag"""
        if not source or 'tag' not in source:
            return None
        if type(source['tag']) == str:
            return [source['tag']]
        elif type(source['tag']) == list:
            return source['tag']
        else:
            return None


class SuiteFileTree(object):
    def __init__(self, lib_path, options):
        if not os.path.exists(lib_path):  # 判断所给路径是否存在
            raise PathError(lib_path)
        if os.path.isfile(lib_path):  # 单文件处理
            self.name = os.path.basename(lib_path).split('.')[0]
            self.root = SuiteFile(self.name, SuiteFile.FILE, suite_file=lib_path)
        elif os.path.isdir(lib_path):  # 文件夹处理
            self.name = os.path.basename(lib_path)
            self.root = SuiteFile(self.name, SuiteFile.DIR)
            self.parse_source(lib_path, self.root)
        else:
            raise FrameWorkError('非文件/目录', lib_path)
        self._parse_selection(options)

    def parse_source(self, source, root):
        """解析目录下的文件"""
        for sub_path in os.listdir(source):
            full_path = os.path.join(source, sub_path)
            if os.path.isdir(full_path):  # 是文件夹时则递归调用该方法
                suite = SuiteFile(sub_path, SuiteFile.DIR, parent=root)
                if len(os.listdir(full_path)) == 0:  # 空目录处理
                    '''warn: miss 空目录'''
                    continue
                else:
                    self.parse_source(full_path, suite)
                if len(suite.child) == 0:
                    '''warn: miss 目录下没有用例文件'''
                root.child.append(suite)
            elif os.path.isfile(full_path):
                if not self._check_type(full_path):  # 若不是yaml文件则跳过，输出警告
                    continue
                if self._parse_file_type(sub_path):  # 检查是否为suite.yml文件
                    root.source_path = full_path
                    root.source = load(full_path)
                    root.tag = root.load_tag(root.source)
                else:
                    root.child.append(SuiteFile(sub_path.split('.')[0],   # 用例文件
                                                SuiteFile.FILE, suite_file=full_path, parent=root))
            else:
                raise FrameWorkError('非文件/目录', full_path)

    def _parse_file_type(self, name):
        """检查是否是资源文件suite.yml"""
        if name.split('.')[0] == 'suite':
            return True
        else:
            return False

    def _check_type(self, sub_path):
        """检查是否是yaml格式的文件"""
        file_type = os.path.basename(sub_path).split('.')[-1]
        if file_type == 'yml':
            return True
        return False

    def _parse_selection(self, options):
        select = options.selection


if __name__ == '__main__':
    print(os.listdir('../../data/abc'))


