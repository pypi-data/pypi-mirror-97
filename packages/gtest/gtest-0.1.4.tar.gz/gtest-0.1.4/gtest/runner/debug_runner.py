# -*- coding: UTF-8 -*-
from gtest.runner.base_runner import BaseRunner
from gtest.utils.logger import logger
from gtest.keyword_.selenium_ import find_elements
import time


class DebugRunner(BaseRunner):
    def run_case(self, case, _result):
        logger.info('执行用例: {} {}'.format(case.name, case.description))
        print('调试模式,点击<ENTER>继续, 或输入q退出调试:')
        start_time = round(time.time(), 2)
        self.run_setup(case.name, case.setup, '用例')
        logger.add_prefix()
        result = list()
        try:
            result = [self.run_step(step) for step in case.step]
        except Exception as e:
            result.append(False)
            self._input('发生异常，点击<ENTER>继续')
            raise e
        finally:
            logger.sub_prefix()
            self.refresh_dyn()
            if False not in result:
                _result['result'] = True
                self.pass_count += 1
                logger.debug('用例执行成功: {} {}, 用时: {}'.format(case.name, case.description, self._count_time(start_time)))
            else:
                _result['result'] = False
                logger.debug('用例执行失败: {} {}, 用时: {}'.format(case.name, case.description, self._count_time(start_time)))
            self.run_teardown(case.name, case.teardown, '用例(Case)')
            '''清除浏览器环境，保证在当前窗口中下一个suite执行时有一个新页面和干净的cookies'''
            self._input('再次点击<ENTER>退出测试')
            self._close_and_open()

    def run_step(self, step_info):
        '''innermost run loop, where the step function run actually'''
        '''where the exceptions raise'''
        if step_info.type == 'keyword' or step_info.type == 'assert':  # 运行type为keyword或者assert的步骤
            keyword = step_info.keyword
            by, path = None, None
            for arg in keyword.args:
                if arg['name'] == 'by':
                    by = arg['value']
                elif arg['name'] == 'path':
                    path = arg['value']
            if by:
                root = keyword.keyword_args['root']['value']
                if root:
                    elements = find_elements(self.driver, by, path, root=self._check_value(root, 'normal'))
                else:
                    elements = find_elements(self.driver, by, path)
                first_element = elements.pop(0)
                self.driver.execute_script("arguments[0].style.border = '2px solid red';", first_element)
                for element in elements:
                    self.driver.execute_script("arguments[0].style.border = '2px solid blue';", element)
                logger.info('查找元素: 方法:{}, 路径:{}, 一共匹配{}个，第一个标记为红色，其他标记为蓝色'.format(by, path, len(elements)+1))
                self._input('')

            a = [self._check_value(arg['value'], 'normal') for arg in keyword.args]
            s = ''
            if keyword.keyword_args:
                for name, value in keyword.keyword_args.items():
                    arg = '{}={}'.format(name, self._check_value(value['value'], 'keyword')) if value['value'] else None
                    s += ', ' + arg if arg else ''
            if keyword.inner_args:
                exec_command = 'self.r = keyword.func(self.driver, *a{})'.format(s)
            else:
                exec_command = 'self.r = keyword.func(*a{})'.format(s)
            if hasattr(step_info, 'description') and step_info.description:
                logger.info('执行步骤: 类型{}, 关键字{}, 描述:{}'.format(step_info.type, keyword.name, step_info.description))
            else:
                logger.info('执行步骤: 类型{}, 关键字{}'.format(step_info.type, keyword.name))
            exec(exec_command)
            if step_info.type == 'keyword' and step_info.return_var:
                self.dyn_var[step_info.return_var[0]] = self.r
                self._input('')
                return True
            else:
                self._input('')
                return self.r

    def _input(self, msg):
        s = input(msg)
        if s == 'q':
            exit()
