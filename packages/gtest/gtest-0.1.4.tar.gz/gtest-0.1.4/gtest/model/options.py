# -*- coding: UTF-8 -*-
from gtest.utils.file import load
from gtest.exceptions import *
import os


class BaseOptions(object):
    """该类用于提供类属性作为各个选项的默认值或可选值"""
    '''选项值类型'''
    SWITCH = 0  # 开关参数，即只有True和False
    SINGLE_NAMED = 1  # 单值选项参数，只有固定选项
    SINGLE_STR = 2  # 单值任意参数，参数值任意字符串，多为路径参数
    SINGLE_NUM = 3  # 单值任意参数，参数值为数字
    MULTI_STR = 4  # 多值任意参数，参数值任意字符串，数量任意
    '''所有可选项'''
    options = {
        'run_path':      [SINGLE_STR, None],  # 要执行的用例所在路径
        'driver_path':   [SINGLE_STR, None],  # 浏览器驱动所在路径
        'run_mode':      [SINGLE_NAMED, 'default', ['default', 'debug', 'effect']],  # 运行模式
        'run_time':      [SINGLE_NUM, 1],  # 执行次数
        'rerun':         [SINGLE_NAMED, 'none', ['none', 'all', 'fail', 'fail_all']],  # 重跑策略
        'rerun_time':    [SINGLE_NUM, 1],  # 重跑次数
        'select':        [MULTI_STR, 'all'],  # 筛选条件
        'exclude':       [MULTI_STR, None],  # 排除条件
        'tag':           [MULTI_STR, None],  # 使用标签
        'report':        [SINGLE_NAMED, 'console', ['console', 'html_only', 'json_only', 'con_html']],  # 输出形式
        'report_path':   [SINGLE_STR, None],  # 报告输出路径
        'console_mode':  [SINGLE_NAMED, 'detail', ['quiet', 'default', 'detail']],  # 控制台输出形式
        'track_error': [SWITCH, False],
        'slow': [SWITCH, False]
    }

    @staticmethod
    def check_options(opt, opt_value):
        """检查是否有错误的选项名或者不符合规范的选项值"""
        if opt not in BaseOptions.options:
            if opt != 'option' and opt != '__line__':  # 过滤option参数的情况
                raise NoMatchOptionError(opt)
            else:
                return opt, opt_value
        t = BaseOptions.options[opt][0]
        if t == BaseOptions.MULTI_STR:
            return BaseOptions._parse_multi_str_option(opt, opt_value)
        elif t == BaseOptions.SWITCH:
            return BaseOptions._parse_switch_option(opt, opt_value)
        elif t == BaseOptions.SINGLE_NAMED:
            return BaseOptions._parse_named_options(opt, opt_value)
        elif t == BaseOptions.SINGLE_STR:
            return BaseOptions._parse_single_str_option(opt, opt_value)
        elif t == BaseOptions.SINGLE_NUM:
            return BaseOptions._parse_single_num_option(opt, opt_value)
        else:
            raise FrameWorkError('No match option type!')

    @staticmethod
    def _parse_named_options(opt, opt_value):
        if type(opt_value) == list and len(opt_value) != 1:
            raise ParamAmountError(opt, 1, len(opt_value))
        try:
            opt_value = str.lower(opt_value)
        except TypeError:
            pass
        if opt_value is None or opt_value not in BaseOptions.options[opt][2]:
            raise ParamValueError(opt, opt_value, BaseOptions.options[opt][2])
        return opt, opt_value

    @staticmethod
    def _parse_single_num_option(opt, opt_value):
        if type(opt_value) == list and len(opt_value) != 1:
            raise ParamAmountError(opt, 1, len(opt_value))
        try:
            num = int(opt_value) if type(opt_value) != int else opt_value
        except ValueError:
            raise ParamValueError(opt, opt_value, '1,2,3,4,5')
        if num < 1:  # 不能为None或者小于1
            raise ParamValueError(opt, num, '1,2,3,4,5')
        return opt, num

    @staticmethod
    def _parse_single_str_option(opt, opt_value):
        if type(opt_value) == list and len(opt_value) != 1:
            raise ParamAmountError(opt, 1, len(opt_value))
        return opt, opt_value

    @staticmethod
    def _parse_multi_str_option(opt, opt_value):
        return opt, opt_value

    @staticmethod
    def _parse_switch_option(opt, opt_value):
        if opt_value not in (None, True, False):
            raise ParamValueError(opt, opt_value, 'True||False 或者为空')
        opt_value = True if opt_value is None else opt_value
        return opt, opt_value


class Options(BaseOptions):
    """选项解析类"""
    def __init__(self, path, options, version):
        self.version = version
        for option, value in self.options.items():  # 先保存baseoption中保存的默认值
            setattr(self, option, value[1])
        if options and 'option' in options:  # 先查找命令行参数中是否有指定option文件
            option_path = options.pop('option')
            if not os.path.isfile(option_path):
                raise PathError(option_path)
            else:
                opts = self.load_option_file(option_path)
            for option, value in opts.items():  # 再解析并保存option.yml中的配置
                if option not in options:
                    opt, opt_value = self.check_options(str.lower(option), value)
                    setattr(self, opt, opt_value)
        for option, value in options.items():  # 最后保存命令行参数中的配置，不需要解析，前面已经完成
            setattr(self, option, value)
        self.run_path = path if path else self.run_path
        if self.run_path is None:  # 当run_path还是为None时抛出异常
            raise NoRunPathError()
        self._parse_selection()

    def _parse_selection(self):
        '''
        if self.select != 'all':
            self.selection['select'] = dict()
        for item in self.select:
            now_n = self.selection['select']
            for n in item.split('::'):
                if ',' in n:
                    for m in n.split(','):
                        now_n[m] = None
                else:
                    now_n[n] = dict()
                    now_n = now_n[n]
        if self.exclude != 'none':
            self.selection['select'] = list()
            for item in self.exclude:
                s = item.split('::')
                s[-1] = s[-1].split(',')
                self.selection['exclude'].append(s)
        '''

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def load_option_file(self, path):
        return load(path)

    def _create_model(self):
        raise Exception


if __name__ == '__main__':
    opt = Options({'select': ['TestLogin::TestLoginSuccess, TestPhoneSuccess',
                              'TestLogin::TestLoginSuccess',
                              'mail::TestHomePage::TestLogin'],
                   'exclude': []})
    print()
