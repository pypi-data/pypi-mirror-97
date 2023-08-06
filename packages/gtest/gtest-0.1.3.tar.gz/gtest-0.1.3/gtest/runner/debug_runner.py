# -*- coding: UTF-8 -*-
from gtest.runner.base_runner import BaseRunner
from gtest.utils.logger import logger
import time


class DebugRunner(BaseRunner):
    def run_case(self, case, _result):
        logger.info('执行用例: {} {}'.format(case.name, case.description))
        start_time = round(time.time(), 2)
        self.run_setup(case.name, case.setup, '用例')
        logger.add_prefix()
        result = list()
        try:
            for step in case.step:
                result.append(self.run_step(step))
        except Exception as e:
            result.append(False)
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
            self._close_and_open()

    def run_step(self, step_info):
        '''innermost run loop, where the step function run actually'''
        '''where the exceptions raise'''
        if step_info.type == 'keyword' or step_info.type == 'assert':  # 运行type为keyword或者assert的步骤
            keyword = step_info.keyword
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
            if step_info.description:
                logger.info('执行步骤: 类型{}, 关键字{}, 描述:{}'.format(step_info.type, keyword.name, step_info.description))
            else:
                logger.info('执行步骤: 类型{}, 关键字{}'.format(step_info.type, keyword.name))
            exec(exec_command)
            if step_info.type == 'keyword' and step_info.return_var:
                self.dyn_var[step_info.return_var[0]] = self.r
                return True
            else:
                return self.r