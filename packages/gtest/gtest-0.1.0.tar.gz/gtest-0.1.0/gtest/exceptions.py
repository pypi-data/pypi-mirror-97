# -*- coding: UTF-8 -*-
from gtest.utils.logger import logger
import inspect
import re


class BaseException(Exception):
    def __init__(self, msg, *args):
        attr = ''  # 各种错误信息的string
        for a in self.__dict__:  # 循环从__dict__中获取已_下标开头的错误信息，汇总到attr:str中
            if re.match('_[a-zA-Z_]+', a):
                attr += a.strip('_') + ': ' + str(self.__dict__[a]) + '  '
        class_name = str(type(self)).strip('<\'>').split('.')[-1]
        msg = '<{}>: {}'.format(class_name, msg)
        logger.error([msg, attr, *args])


class DataError(BaseException):
    def __init__(self, msg):
        self.msg = msg


class FileError(BaseException):
    """用于解析目录文件时抛出异常基类"""
    def __init__(self, msg):
        BaseException.__init__(self, msg)


class ContextException(BaseException):
    """用于解析文件内容时抛出异常基类，提供打印异常出现的文件路径和内容上下文"""
    def __init__(self, msg, line):
        stack = inspect.stack()  # 获取调用堆栈
        '''循环判断是否存在parent属性来确定发生异常的解析对象在堆栈中的位置'''
        stack_index = 0
        s = hasattr(stack[stack_index].frame.f_locals['self'], 'parent')
        while not s:
            stack_index += 1
            if 'self' in stack[stack_index].frame.f_locals:
                s = hasattr(stack[stack_index].frame.f_locals['self'], 'parent')
            else:
                s = None
        local_cls = stack[stack_index].frame.f_locals['self']
        '''获取suite'''
        from gtest.model.suite_tree import Suite
        root = local_cls
        while type(root) != Suite and root.parent is not None:
            root = root.parent
        '''打印原suite对应的文件路径'''
        self._suite = root.get_parent_name()  # 发生错误的SuiteName
        '''打印错误在原文件的上下文'''
        from gtest.utils.file import get_context
        context = get_context(root.source_path, line)
        BaseException.__init__(self, msg, *context)


class FrameWorkError(BaseException):
    """用于内部调试，永远都不能引发"""
    def __init__(self, *args):
        self.msg = '框架异常，请通知作者'
        self._arg = args
        BaseException.__init__(self, self.msg)

# =============================================
# 命令行参数异常 || option文件格式错误


class EssentialParamError(BaseException):
    """命令行必要参数缺失或者异常"""
    def __init__(self):
        self.msg = '开头至少要有一个参数<run_path>用于指定测试路径或者使用 -o||--option <file_path> 指定配置文件'
        BaseException.__init__(self, self.msg)


class NoMatchArgError(BaseException):
    """没有匹配的命令行参数"""
    def __init__(self, arg):
        self.msg = '没有匹配的参数: {}'.format(arg)
        BaseException.__init__(self, self.msg)


class ParamAmountError(BaseException):
    """选项值数量不匹配"""
    def __init__(self, opt, require, given):
        self.msg = '选项 {} 需要 {} 个选项值，但给出 {} 个选项值'.format(opt, require, given)
        BaseException.__init__(self, self.msg)


class ParamValueError(BaseException):
    """选项值不正确"""
    def __init__(self, opt, given, suggest):
        self.msg = '选项 {} 的选项值 {} 不正确，参考值: {}'.format(opt, given, suggest)
        BaseException.__init__(self, self.msg)


class NoRunPathError(BaseException):
    """option文件缺少run_path"""
    def __init__(self):
        self.msg = 'run_path或者option.yml中的run_path二者不能同时为空'
        BaseException.__init__(self, self.msg)


class NoMatchOptionError(BaseException):
    """没有匹配的option的项"""
    def __init__(self, opt):
        self.msg = '没有匹配的选项: {}'.format(opt)
        BaseException.__init__(self, self.msg)

# ===============================================


class PathError(FileError):
    """指定的path不存在"""
    def __init__(self, path):
        self.msg = '路径不存在'
        self._path = path
        FileError.__init__(self, self.msg)


class MissAttrError(ContextException):
    """必要字段缺失"""
    def __init__(self, place, attr, usage, line):
        self.msg = '{} 需要字段 <{}> 用于{}'.format(place, attr, usage)
        ContextException.__init__(self, self.msg, line)


class UseAttrError(ContextException):
    """禁止出现的字段"""
    def __int__(self, place, attr, line):
        self.msg = "{} 不能出现字段 {}".format(place, attr)
        ContextException.__init__(self, self.msg, line)


class NoneAttrError(ContextException):
    """字段不能为空"""
    def __init__(self, place, attr, line):
        self.msg = '{} 的 <{}> 不能为空'.format(place, attr)
        ContextException.__init__(self, self.msg, line)


class AttrTypeError(ContextException):
    """字段值为不支持类型"""
    def __init__(self, place, attr, _type, line):
        self.msg = '{} 的 <{}> 只支持{}'.format(place, attr, _type)
        ContextException.__init__(self, self.msg, line)


class CliArgError(BaseException):
    """命令行参数错误"""
    def __init__(self, msg):
        BaseException.__init__(self, msg)


class OutOfRangeError(ContextException):
    """引用变量下标越界"""
    def __init__(self):
        pass


class VarNotFoundError(ContextException):
    """引用的变量未找到"""
    def __init__(self, msg, line):
        ContextException.__init__(self, msg, line)


class TypeError(ContextException):
    """字段内容的格式不符"""
    def __init__(self, _type, required_type, line):
        ContextException.__init__(self, '<{}>下的字段应该为{}'.format(_type, required_type), line)


# 未找到该关键字
class KeyWordNoFound(BaseException):
    def __init__(self, _keyword):
        self.keyword = _keyword


class ElementNoFound(BaseException):
    def __init__(self, by, path):
        self.msg = '元素未找到, 定位信息:{}, {}'.format(by, path)
        BaseException.__init__(self, self.msg)


class YamlParseError(BaseException):
    """Pyyaml解析错误抛出的异常"""
    def __init__(self, error):
        self.msg = error.__context__
        BaseException.__init__(self, self.msg)


class RuntimeArgNoFound(BaseException):
    """引用了不存在的返回值"""
    def __init__(self, arg):
        self.msg = '引用了不存在的返回值: {}'.format(arg)
        BaseException.__init__(self, self.msg)
