# -*- coding: UTF-8 -*-
from gtest.exceptions import *
import re


class VarMatcher(object):
    @staticmethod
    def keyword_args_match(args):
        if args is None:
            return [], {}
        la = list()
        lb = dict()
        for arg in args:
            if re.match('^[a-zA-Z0-9_]+=[+${}a-zA-Z0-9_"]+$', arg):
                a = arg.replace('"', '').split('=')
                lb[a[0]] = a[1]
            else:
                la.append(arg)
        return la, lb

    @staticmethod
    def args_match(arg):
        if re.match('^\$[a-zA-Z0-9_]?{[a-zA-Z0-9_]+}(\[[0-9][0-9]?\])?$', arg):
            s = arg.split('}')
            group, var = s[0].replace('$', '').split('{')
            index = int(s[1].strip('[]')) if '[' in s[1] else None
            group = None if group == '' else group
        else:
            return None
        return group, var, index

    @staticmethod
    def inner_args_match(arg, caller):
        if arg is None:
            return arg
        pattern = re.compile('\+\$[a-zA-Z0-9_]?{[a-zA-Z0-9_]+}(\[[0-9][0-9]?\])?')
        _arg = arg
        while pattern.search(_arg) is not None:
            match = pattern.search(_arg).group()
            s = match.split('}')
            group, var = s[0].replace('+$', '').split('{')
            index = int(s[1].strip('[]')) if '[' in s[1] else None
            group = None if group == '' else group
            _arg = _arg.replace(match, caller.get('vars', group, var, index)['value'])
        return _arg

    @staticmethod
    def runtime_arg_match(arg):
        if re.match('^\${[a-zA-Z0-9_]+}(\[[0-9][0-9]?\])?$', arg):
            arg = arg.replace('${', '')
            arg = arg.replace('}', '')
            return arg
        else:
            return None


if __name__ == '__main__':
    print(VarMatcher.inner_args_match('open_url="https://+${pr34id}[0].runj+${pr3id}[0].cn"', a))
