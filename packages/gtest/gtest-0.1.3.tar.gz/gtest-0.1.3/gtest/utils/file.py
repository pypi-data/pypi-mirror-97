# -*- coding: UTF-8 -*-
from itertools import islice

from gtest.exceptions import *
import os.path
import yaml
from yaml.parser import ParserError


def load(path):
    if not os.path.isfile(path):
        raise FrameWorkError('load path must be file')
    t = os.path.basename(path).split('.')[1]
    with open(path, 'rb') as f:
        try:
            data = yaml.load(f, Loader=LineLoader)
        except ParserError:
            raise YamlParseError
    return data


def get_context(path, line_num, scope=8, highlight=False):
    msgs = ['》》》》错误所在上下文：']
    with open(path, encoding='utf-8') as f:
        line_n = line_num-scope if line_num-scope >= 0 else 0
        for line in islice(f, line_n, line_num+scope):
            if highlight:
                s = '\033[1;31m' + str(line_n+1) + ': ' + line.strip('\n') if line_n == line_num else '\033[0m' + \
                                                                                          str(line_n + 1) + ': ' + line
            else:
                s = '\033[0m' + str(line_n + 1) + ': ' + line.strip('\n')
            msgs.append(s)
            line_n += 1
    return msgs


class LineLoader(yaml.Loader):
    def construct_mapping(self, node, deep=False):
        mapping = super(LineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


if __name__ == '__main__':
    load('')
