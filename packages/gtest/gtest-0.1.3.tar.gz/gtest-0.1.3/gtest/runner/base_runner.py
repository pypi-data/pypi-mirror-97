# -*- coding: UTF-8 -*-
from contextlib import contextmanager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from gtest.utils.logger import logger
from gtest.model.matcher.var_matcher import VarMatcher
from gtest.exceptions import *
import time


class BaseRunner:

    def __init__(self, suite_tree, option):
        self.option = option
        self.result = {'lib_name': suite_tree.root.name}
        self.r = None  # 用于传递到exec函数中做返回值的变量
        self.dyn_var = dict()  # 用于保存运行时变量
        self.case_count = 0  # 用例计数
        self.pass_count = 0  # 成功用例计数
        '''保存所有待执行的suite，包括其自身合父suite的setup/teardown，'''
        '''把树性的组织结构转化为列表的形式，以suite为单位进行执行'''
        self.suite_list = list()
        self.driver = None
        '''收集可执行Suite和用例'''
        self.collect_case(suite_tree, self.result, self.suite_list)
        logger.debug('收集到 {} 个Suite，总共 {} 个用例！'.format(len(self.suite_list), self.case_count))
        '''执行用例'''
        '''miss: driver管理器'''
        '''当前默认管理一个driver， 待更新'''
        '''
        self.driver = None
        for suite in self.suite_list:
            for case in suite['cases']:
                for step in case.step:
                    r = self.run_step(step)
                    print(r)
        print('a')
        '''
        try:
            with self.run_session():
                for suite in self.suite_list:
                    self.run_suite(suite)
        except Exception as e:
            raise e
        finally:
            logger.info('测试结束，测试成功 {} 个用例，失败 {} 个用例'.format(self.pass_count, self.case_count-self.pass_count))
        print()

    def collect_case(self, suite_tree, result, suite_list):
        self._collect_case(suite_tree.root, result, suite_list)
        self.suite_list.reverse()

    def _collect_case(self, s_node, r_node, suite_list):
        """统计case，保存到待执行列表和result列表中"""
        if hasattr(s_node, 'cases') and s_node.cases is not None:
            r_node['cases'] = list()
            for case in s_node.cases:
                self.case_count += 1
                r_node['cases'].append({'name': case.name,
                                        'description': case.description if hasattr(case, 'description') else None,
                                        'result': None})
            suite_list.append({'name': s_node.name,
                               'cases': s_node.cases,
                               'setup': self._get_pre_and_post(s_node, 'setup'),
                               'teardown': self._get_pre_and_post(s_node, 'teardown'),
                               'case_setup': s_node.case_setup,
                               'case_teardown': s_node.case_teardown,
                               'result': r_node['cases']})
        else:
            r_node['child'] = list()
            for child in s_node.child:
                child_d = {'name': child.name}
                self._collect_case(child, child_d, suite_list)
                r_node['child'].append(child_d)

    def _get_pre_and_post(self, s_node, _type):
        l = list()
        c_node = s_node
        l.insert(0, getattr(c_node, _type))
        while c_node.parent is not None:  # 循环查找其父suite是否有setup/teardown
            c_node = c_node.parent
            l.insert(0, getattr(c_node, _type))
        l = [item for item in l if item is not None]  # 去除值为None的setup/teardown
        return l

    @contextmanager
    def run_session(self):
        """miss：目前主要用于启动和关闭浏览器"""
        self.driver = self.load_driver()
        logger.info('启动浏览器: {}, 版本: {}')
        self.driver.maximize_window()
        try:
            yield
        except Exception as e:
            raise e
        finally:
            self.driver.quit()
            logger.info('关闭浏览器')

    def run_suite(self, suite):
        logger.info('执行测试套件: {}'.format(suite['name']))
        self.run_setup(suite['name'], suite['setup'], '测试套件')
        logger.add_prefix()
        try:
            for i in range(0, len(suite['cases'])):
                self.run_case(suite['cases'][i], suite['result'][i])
        except Exception as e:
            raise e
        finally:
            logger.sub_prefix()
            self.run_teardown(suite['name'], suite['teardown'], '测试套件')
            '''清除浏览器环境，保证在当前窗口中下一个suite执行时有一个新页面和干净的cookies'''
            self._delete_close_and_open()

    def run_case(self, case, _result):
        pass

    def run_setup(self, name, setups, _type):
        if not setups:
            return
        logger.info('执行{}:<{}>的前置操作:'.format(_type, name))
        logger.add_prefix()
        try:
            if _type == '测试套件':
                for setup in setups:
                    for step in setup:
                        self.run_step(step)
            elif _type == '用例':
                for step in setups:
                    self.run_step(step)
        finally:
            logger.sub_prefix()
            self.refresh_dyn()

    def run_teardown(self, name, teardown, _type):
        if not teardown:
            return
        logger.info('执行{}:<{}>的后置操作:'.format(_type, name))
        logger.add_prefix()
        try:
            for step in teardown:
                self.run_step(step)
        finally:
            logger.sub_prefix()
            self.refresh_dyn()

    def run_step(self, step_info):
        '''innermost run loop, where the step function run actually'''
        '''where the exceptions raise'''
        if self.option.slow:
            time.sleep(1)
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
            if hasattr(step_info, 'description') and step_info.description:
                logger.info('执行步骤: 类型{}, 关键字{}, 描述:{}'.format(step_info.type, keyword.name, step_info.description))
            else:
                logger.info('执行步骤: 类型{}, 关键字{}'.format(step_info.type, keyword.name))
            exec(exec_command)
            if step_info.type == 'keyword' and step_info.return_var:
                self.dyn_var[step_info.return_var[0]] = self.r
                return True
            else:
                return self.r

    # 关闭窗口删除cookies并打开新的窗口（适用于登录注册）
    def _delete_close_and_open(self):
        '''
        self.driver.delete_all_cookies()  # 清除cookies
        self.driver.execute_script('window.open()')
        self.driver.close()
        time.sleep(1)
        input()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        '''
        self.driver.quit()
        self.driver = self.load_driver()

    # 关闭窗口并打开新的窗口
    def _close_and_open(self):
        self.driver.execute_script('window.open()')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def _count_time(self, start_time):
        end_time = round(time.time(), 2)
        use_time = end_time - start_time
        m = int(use_time / 60)
        s = round(use_time % 60, 2)
        return '{}分{}秒'.format(m, s)

    def _check_value(self, value, _type):
        """检查参数是否包含动态变量并给出值"""
        v = VarMatcher.runtime_arg_match(value)
        if v:
            if v in self.dyn_var:
                if _type == 'normal':
                    return self.dyn_var[v]
                elif _type == 'keyword':
                    return 'self.dyn_var["{}"]'.format(v)
            else:
                raise RuntimeArgNoFound(v)
        else:
            return value

    def refresh_dyn(self):
        self.dyn_var = dict()

    def load_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.option.driver_path:
            '''如果有指定driver_path参数，则忽略其他地址，出现异常直接raise'''
            driver = WebDriver(executable_path=self.option.driver_path, options=chrome_options)
            return driver
        import os
        driver_file = None
        if os.path.isdir(self.option.run_path):  # 检查run_path下是否有driver文件
            driver_file = None
            for file in os.listdir(self.option.run_path):
                if file.startswith('chromedriver'):
                    driver_file = file
        if driver_file:
            try:
                driver = WebDriver(executable_path=os.path.join(self.option.run_path, driver_file), options=chrome_options)
            except WebDriverException:
                driver = WebDriver(options=chrome_options)
        else:
            driver = WebDriver(options=chrome_options)
        return driver


def RunnerFactory(run_mode, suite_tree, option):
    if run_mode == 'default':
        from gtest.runner.default_runner import DefaultRunner
        return DefaultRunner(suite_tree, option)
    elif run_mode == 'debug':
        from gtest.runner.debug_runner import DebugRunner
        return DebugRunner(suite_tree, option)
