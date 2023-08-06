# -*- coding: UTF-8 -*-:
import setuptools
from gtest.gtest import GTest

setuptools.setup(
    name='gtest',
    version=GTest.version,
    author='NiKoChen',
    author_email='NiKoChen2649@gmail.com',
    description='A Automatic Test FrameWork',
    url='https://gitee.com/CMTY/gtiee_-test',
    packages=setuptools.find_packages(),
    python_requires='>=3',
    license='MIT',
    install_requires=['PyYAML>=5', 'selenium>=3'],  # 目前只需要这两个依赖包，对版本要求不严格，但为了避免未知的异常还是已目前最高版本限制
    entry_points={'console_scripts': ['gtest = gtest.gtest:run_from_cli']}  # 自动生成script到python/scripts下
)
