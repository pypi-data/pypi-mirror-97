# -*- coding: UTF-8 -*-s
import os


class Console(object):
    def __init__(self):
        try:
            weight = os.get_terminal_size().columns   # 获取控制台宽度
        except OSError:
            weight = 50  # 使用pycharm或其他IDE无法获取宽度，直接指定一个默认值

    def print(self, msg):
        self._print(msg)

    def _print(self, msg):
        if msg == list:
            for m in msg:
                print(m)
        else:
            print(msg)

