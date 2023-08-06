# -*- coding: UTF-8 -*-
from gtest.utils.logger import logger
from gtest.utils.console import Console
import os


class Output(object):
    ERROR = 0
    OPERATE = 1

    def __init__(self, option):
        self.logger = logger
        self.console = Console()

    def error(self, msg):
        self.console.print(msg)