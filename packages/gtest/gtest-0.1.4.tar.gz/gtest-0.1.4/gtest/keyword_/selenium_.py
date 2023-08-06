# -*- coding: UTF-8 -*-
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common import exceptions as ex
from gtest.exceptions import *
time_out = 5


By = {'id': By.ID,
      'name': By.NAME,
      'class': By.CLASS_NAME,
      'xpath': By.XPATH,
      'link_text': By.LINK_TEXT,
      'tag': By.TAG_NAME}

'''#####用于操作的方法##################################################################################################'''


# 查找当个元素
def find_element(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: element 获取到的元素
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        if root:
            element = wait(root, timeout).until(lambda x: x.find_element(By[by], path))
        else:
            element = wait(driver, timeout).until(lambda x: x.find_element(By[by], path))
        driver.execute_script("arguments[0].style.border = '2px solid red';", element)
    except ex.TimeoutException:
        raise ElementNoFound(By[by], path)
    else:
        return element


# 查找一组元素
def find_elements(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素组的方式
    :param path: 查找元素组的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: elements 获取到的元素组
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        if root:
            elements = wait(root, timeout).until(lambda x: x.find_elements(By[by], path))
        else:
            elements = wait(driver, timeout).until(lambda x: x.find_elements(By[by], path))
    except ex.TimeoutException as t:
        raise ElementNoFound(By[by], path)
    else:
        return elements


# 输入文本/值
def send_key(driver, by, path, msg, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :param msg: 要输入到元素中的文本值
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: element 获取到的元素
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        element = find_element(driver, By[by], path, timeout=timeout, root=root)
        element.clear()
        element.send_keys(msg)
    except ex.TimeoutException:
        raise ElementNoFound(By[by], path)
    else:
        return element


# 点击元素
def click_element(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: element 获取到的元素
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        element = find_element(driver, by, path, timeout=timeout, root=root)
    except ex.TimeoutException:
        raise ElementNoFound(By[by], path)
    try:
        element.click()
    except ex.ElementNotInteractableException:
        try:
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            raise e
    return element


# 悬停在元素上
def hover_element(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: element 获取到的元素
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    element = find_element(driver, By[by], path, timeout=timeout, root=root)
    try:
        ActionChains(driver).move_to_element(element).perform()
    except ex.TimeoutException:
        raise ElementNoFound(By[by], path)
    else:
        return element


# 刷新页面
def refresh(driver):
    """
    :inner_param driver: Web驱动
    """
    driver.refresh()


# 删除所有cookie
def del_cookies(driver):
    """
    :inner_param driver: Web驱动
    """
    driver.delete_all_cookies()
    import time
    time.sleep(1)


# 打开网站
def open_url(driver, test_url):
    """
    :inner_param driver: Web驱动
    :param test_url: 要打开的网页URL
    """
    driver.execute_script('window.location.href="{url_}"'.format(url_=test_url))


'''=================================================================================================================='''
'''=====用于断言的方法=================================================================================================='''


# 判断元素是否存在
def is_element_exist(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: bool 判定值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        if root:
            wait(root, timeout). \
                until(conditions.visibility_of_element_located((By[by], path)))
        else:
            wait(driver, timeout). \
                until(conditions.visibility_of_element_located((By[by], path)))
    except ex.TimeoutException:
        return False
    else:
        return True


# 检查元素是否可以点击了
def element_to_be_clickable(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: bool 判定值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        if root:
            wait(root, timeout). \
                until(conditions.element_to_be_clickable((By[by], path)))
        else:
            wait(driver, timeout). \
                until(conditions.element_to_be_clickable((By[by], path)))
    except ex.TimeoutException:
        return False
    else:
        return True


# 判断元素是否被选择
def element_to_be_selected(driver, by, path, timeout=time_out, root=None):
    """
    :inner_param driver:  Web驱动
    :param by: 查找元素的方式
    :param path: 查找元素的路径
    :keyword_param timeout: 超时时间
    :keyword_param root: 指定父元素作为查找范围
    :return: bool 判定值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        if root:
            wait(root, timeout). \
                until(conditions.element_to_be_selected((By[by], path)))
        else:
            wait(driver, timeout). \
                until(conditions.element_to_be_selected((By[by], path)))
    except ex.TimeoutException:
        return False
    else:
        return True


# 判断页面是否改变
def is_url_change(driver, url, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :param url: 要检查的页面URL
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.url_changes(url))
    except ex.TimeoutException:
        return False
    else:
        return True


# 判断页面是否包含‘xxx’
def if_url_contains(driver, url, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :param url: 要检查的页面URL
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.url_contains(url))
    except ex.TimeoutException:
        return False
    else:
        return True


# 判断页面是否匹配‘xxx’(正则表达式)
def if_url_matches(driver, url, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :param url: 要检查的页面URL
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.url_matches(url))
    except ex.TimeoutException:
        return False
    else:
        return True


# 检查页面标题是否含‘xxx’
def if_title_contains(driver, title, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :param title: 要检查的页面title
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.title_contains(title))
    except ex.TimeoutException:
        return False
    else:
        return True


# 检查页面标题是否为‘xxx’
def if_title_is(driver, title, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :param title: 要检查的页面title
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.title_is(title))
    except ex.TimeoutException:
        return False
    else:
        return True


# 检查是否有alert框弹出
def alert_is_present(driver, timeout=time_out):
    """
    :inner_param driver:  Web驱动
    :keyword_param timeout: 超时时间
    :return: bool 判断值
    """
    timeout = timeout if type(timeout) == int else int(timeout)
    try:
        wait(driver, timeout).until(conditions.alert_is_present())
    except ex.TimeoutException:
        return False
    else:
        return True


'''=================================================================================================================='''


keyword = {'find_element': find_element,
           'find_elements': find_elements,
           'hover': hover_element,
           'send_key': send_key,
           'click': click_element,
           'refresh': refresh,
           'del_cookies': del_cookies,
           'open_url': open_url,
           'is_element_exist': is_element_exist,
           'can_be_clickable': element_to_be_clickable,
           'be_selected': element_to_be_selected,
           'if_url_change': is_url_change,
           'if_url_contains': if_url_contains,
           'if_url_matches': if_url_matches,
           'if_title_contains': if_title_contains,
           'if_title_is': if_title_is,
           'if_alert_is_present': alert_is_present}
