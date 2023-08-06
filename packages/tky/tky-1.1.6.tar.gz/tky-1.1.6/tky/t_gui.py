# _*_ coding:utf-8 _*_
"""
常用GUI类集合
\n 目前支持的有：
\n t_click （点击事件）
\n t_clear （清除事件）
\n t_send_keys （输入事件）
\n wait_one （元素扫描）
\n @author: 'TangKaiYue'
"""

import datetime
from .t_jde import null
import selenium.webdriver.support.ui as ui  # 页面元素检查


# 扫描元素并执行-点击事件
def t_click(name: str = 'null', value: str = 'null', driver: str = 'null', sed: int = 10):
    """
    [GUI元素扫描并点击事件]\n
    :param name: str 要查询的类，如ID/NAME/CLASS/XPATH；
    :param value: str 具体的元素值；
    :param driver: str 具体的driver值；
    :param sed: int 要扫描的时长(秒),默认10S；
    :return: 执行点击操作
    """
    try:
        if null(name) == 'N' or null(value) == 'N' or null(driver) == 'N':
            return print("入参异常：查询类，具体值，driver值 不能为空...")
        print('click - type==%s ，value==%s ，time==%s' % (name, value, datetime.datetime.now()))
        if name == 'id':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_id(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_id(value).click()  # 执行操作
        if name == 'name':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_name(value).click()  # 执行操作
        if name == 'class_name':
            ui.WebDriverWait(driver, sed).until(
                lambda w: driver.find_element_by_class_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_class_name(value).click()  # 执行操作
        if name == 'xpath':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_xpath(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_xpath(value).click()  # 执行操作
    except EnvironmentError as err:
        return '发生异常：%s' % err


# 扫描元素并执行-清除事件(name请传入要查询的类，如ID/NAME/CLASS/XPATH；value请传入具体的值；)
def t_clear(name: str = 'null', value: str = 'null', driver: str = 'null', sed: int = 10):
    """
    [GUI元素扫描并点击事件]\n
    :param name: str 要查询的类，如ID/NAME/CLASS/XPATH；
    :param value: str 具体的元素值；
    :param driver: str 具体的driver值；
    :param sed: int 要扫描的时长(秒),默认10S；
    :return: 执行清除操作
    """
    try:
        if null(name) == 'N' or null(value) == 'N' or null(driver) == 'N':
            return print("入参异常：查询类，具体值，driver值 不能为空...")
        print('clear - type==%s ，value==%s ，time==%s' % (name, value, datetime.datetime.now()))
        if name == 'id':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_id(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_id(value).clear()  # 执行操作
        if name == 'name':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_name(value).clear()  # 执行操作
        if name == 'class_name':
            ui.WebDriverWait(driver, sed).until(
                lambda w: driver.find_element_by_class_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_class_name(value).clear()  # 执行操作
        if name == 'xpath':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_xpath(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_xpath(value).clear()  # 执行操作
    except EnvironmentError as err:
        return '发生异常：%s' % err


# 扫描元素并执行-输入事件(name请传入要查询的类，如ID/NAME/CLASS/XPATH；value请传入具体的值；key请传入具体的内容；)
def t_send_keys(name: str = 'null', value: str = 'null', key: str = 'null', driver: str = 'null', sed: int = 10):
    """
    [GUI元素扫描并点击事件]\n
    :param name: str 要查询的类，如ID/NAME/CLASS/XPATH；
    :param value: str 具体的元素值；
    :param key: str 要输入的内容；
    :param driver: str 具体的driver值；
    :param sed: int 要扫描的时长(秒),默认10S；
    :return: 执行输入事件
    """
    try:
        if null(name) == 'N' or null(value) == 'N' or null(key) == 'N' or null(driver) == 'N':
            return print("入参异常：查询类，具体值，driver值 不能为空...")
        print('send_keys - type==%s ，value==%s ，values==%s ，time==%s' % (name, value, key, datetime.datetime.now()))
        if str(name) == 'id':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_id(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_id(value).send_keys(key)  # 执行操作
        if str(name) == 'name':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_name(value).send_keys(key)  # 执行操作
        if str(name) == 'class_name':
            ui.WebDriverWait(driver, sed).until(
                lambda w: driver.find_element_by_class_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_class_name(value).send_keys(key)  # 执行操作
        if str(name) == 'xpath':
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_xpath(value))  # 10秒内每隔500毫秒扫描1次页面变化
            driver.find_element_by_xpath(value).send_keys(key)  # 执行操作
    except EnvironmentError as err:
        return '发生异常：%s' % err


# 设定元素扫描(单数)
def wait_one(name: str = 'null', value: str = 'null', driver: str = 'null', sed: int = 10):
    """
    [GUI元素扫描并点击事件]\n
    :param name: str 要查询的类，如ID/NAME/CLASS/XPATH；
    :param value: str 具体的元素值；
    :param driver: str 具体的driver值；
    :param sed: int 要扫描的时长(秒),默认10S；
    :return: 执行元素扫描
    """
    try:
        if null(name) == 'N' or null(value) == 'N' or null(driver) == 'N':
            return print("入参异常：查询类，具体值，driver值 不能为空...")
        print('scanning - type==%s ，value==%s ，time==%s' % (name, value, datetime.datetime.now()))
        if str(name) == str('id'):
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_id(value))  # 10秒内每隔500毫秒扫描1次页面变化
        if str(name) == str('name'):
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
        if str(name) == str('class_name'):
            ui.WebDriverWait(driver, sed).until(
                lambda w: driver.find_element_by_class_name(value))  # 10秒内每隔500毫秒扫描1次页面变化
        if str(name) == str('xpath'):
            ui.WebDriverWait(driver, sed).until(lambda w: driver.find_element_by_xpath(value))  # 10秒内每隔500毫秒扫描1次页面变化
    except EnvironmentError as err:
        return '发生异常：%s' % err
