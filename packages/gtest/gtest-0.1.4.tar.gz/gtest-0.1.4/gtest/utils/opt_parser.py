# -*- coding: UTF-8 -*-
from gtest.exceptions import *
from gtest.model.options import BaseOptions
from gtest.utils.create_template import create_template


class OptionParser(object):
    """命令行参数解析类"""
    '''所有可选命令行参数'''
    options = {
        '--option': '-o',
        '--run_mode': '-m',
        '--run_time': None,
        '--rerun': None,
        '--rerun_time': None,
        '--select': '-s',
        '--exclude': '-e',
        '--tag': '-t',
        '--report': '-r',
        '--report_path': None,
        '--console_mode': '-c',
        '--driver_path': '-d',
        '--track_error': '-T',
        '--slow': '-S',
        'init': None
               }

    def __init__(self):
        self.option_selection = {key.strip('v_'): value for key, value in BaseOptions.__dict__.items()
                                 if key.startswith('v_')}

    def parse(self, args):
        try:
            path, opts = self._parse(args)
        except Exception as e:
            exit()
        else:
            return path, opts


    def _parse(self, args):
        """解析命令行参数"""
        '''处理开头的必要的参数'''
        if args:
            if 'init' == args[0]:  # 第一个参数匹配init的话，不处理后面的所有参数因为无效
                create_template()
            elif self.search_prefix(args[0]):
                if args[0] == '-o' or args[0] == '--option':
                    path = None
                else:
                    raise EssentialParamError()
            else:
                path = args.pop(0)
        else:
            raise EssentialParamError()
        '''循环解析剩下的命令行参数'''
        opts, i, l = dict(), 0, len(args)  # opts:保存解析好的参数
        while i < l:
            opt = self.match_opt(args[i])
            opt_value = list()
            i += 1
            while i < l:
                if not self.search_prefix(args[i]):
                    opt_value.append(args[i])
                    i += 1
                else:
                    break
            if len(opt_value) == 0:
                opt_value = None
            elif len(opt_value) == 1:
                opt_value = opt_value[0]
            o, v = BaseOptions.check_options(opt, opt_value)
            opts[o] = v
        return path, opts

    def match_opt(self, arg):
        """匹配对应的参数"""
        if arg in self.options:
            return arg.strip('-')
        else:
            for opt, value in self.options.items():
                if arg == value:
                    return opt.strip('-')
            raise NoMatchArgError(arg)

    def search_prefix(self, arg):
        if arg.startswith('-') or arg.startswith('--'):
            return True
        return False
