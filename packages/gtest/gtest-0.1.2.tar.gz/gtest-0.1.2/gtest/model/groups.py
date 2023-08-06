# -*- coding: UTF-8 -*-
from gtest.model.matcher.matcher import Matcher
from gtest.exceptions import *
from gtest.utils.common import search_line, lower
import yaml


class Group(object):
    def __init__(self, source, groups):
        self.var = dict()
        self.parent = groups
        self.source = lower(source)
        exec_list = Matcher.match(self.GroupKey, source, self._deal, self)  # 匹配字段
        for e in exec_list:
            e[0](self, e[2])

    def _deal(self, source):
        if type(source) != dict:
            raise AttrTypeError('变量分组', 'group', '键值对', search_line(source))
        if 'group' not in source:
            raise MissAttrError('变量分组', 'group', '指定分组名', search_line(source))
        if source['group'] is None:
            raise NoneAttrError('变量分组', 'group', search_line(source))
        return source

    def add(self, name, value):
        self.__dict__[name] = value

    def get(self, key, index):
        if key in self.var:
            v = dict(self.var[key])
            if index is not None:
                if -1 < index < len(v['value']):
                    v['value'] = v['value'][index]
                else:
                    '''miss: 越界处理'''
                    raise OutOfRangeError()
            return v
        return None

    def _parse_var(self, source):
        s_type = type(source)
        if s_type == dict:
            source = [source]
        elif s_type == list:
            pass
        else:
            raise AttrTypeError('group: {}'.format(self.name), 'var', '键值对或者数组', search_line(source))
        for item in source:
            item = lower(item)
            if 'name' not in item:
                raise MissAttrError('变量分组{}里的变量'.format(self.name), 'name', '指定变量名',  search_line(source))
            elif item['name'] is None:
                raise NoneAttrError('变量分组{}里的变量'.format(self.name), 'name', search_line(source))
            if 'value' not in item:
                raise MissAttrError('变量分组{}里的变量{}'.format(self.name, item['name']), 'value', '指定变量值',  search_line(source))
            elif item['value'] is None or len(item['value']) == 0:
                raise NoneAttrError('变量分组{}里的变量{}'.format(self.name, item['name']), 'value', search_line(source, item['name']))
            self.var[item['name']] = {'description': item['desc'] if 'desc' in item else None,
                                      'value': item['value']}


        """支持的字段    对应方法                               执行顺序(正序)"""
    GroupKey = {
        'group':       [(lambda caller, x:caller.add('name', x)),     1],
        'desc':        [(lambda caller, x:caller.add('desc', x)),     2],
        'remark':      [(lambda caller, x:caller.add('remark', x)),   3],
        'var':         [(lambda caller, x:caller._parse_var(x)),     4]
    }


class DynGroup(object):
    def __init__(self, groups):
        self.parent = groups
        self.case = list()
        self.template = list()

    def set(self, t, *args):
        for var in args:
            getattr(self, t).append(var)

    def get(self, key, index):
        for var in self.case:
            if key == var:
                return {'name': key, 'value': '${%s}' % key, 'description': 'dynamic_var', 'group': None}
        for var in self.template:
            if key == var:
                return {'name': key, 'value': '${%s}' % key, 'description': 'dynamic_var', 'group': None}

    def clear(self, t):
        getattr(self, t).clear()


class Groups(object):
    def __init__(self, source, suite):
        self.parent = suite
        self.remark, self.group = dict(), dict()
        self.dyn_group = DynGroup(self)  # 动态变量池
        self.source = source
        if not source:  # 如果source为None，则返回，只保留动态变量池
            return
        for item in source:
            group = Group(item, self)
            self.group[group.name] = group
            if hasattr(group, 'remark') and group.remark:
                self.remark[group.remark] = group

    def get(self, _group, key, index=None):
        if _group is None:
            var = self.dyn_group.get(key, index)  # 如果没指定group， 先查询动态变量池
            if var:
                return var
            _group = 'default'  # 没指定group，不是动态变量，则为默认变量
        if _group in self.group:  # 先按全称查找
            return self.group[_group].get(key, index)
        elif _group in self.remark:  # 再按别称查找
            return self.remark[_group].get(key, index)
        return None

    def set(self, t, *args):
        self.dyn_group.set(t, *args)

    def clear(self, t):
        self.dyn_group.clear(t)


"""
    ###### test_code ############################################################################
"""


if __name__ == '__main__':
    with open('../../data/gitee/TestLogin.yml', 'rb') as f:
        data = yaml.load(f)
        g = Groups(data['variables'], None)
        print(g.get('U', 'ur_pwd'))
        print()



