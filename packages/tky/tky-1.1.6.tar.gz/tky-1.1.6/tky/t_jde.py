# _*_ coding:utf-8 _*_
"""
常用判断类集合
\n 目前支持方法有：
\n null (数据空判断)
\n val_list （数据匹配，自有；依赖re）
\n @author: 'TangKaiYue'
"""

import re


# 数据空判断
def null(val: str = 'null'):
    """
    数据为空判断;
    :param val : str 传入的内容；
    :return 为空输出'N'，不为空则输出传入内容；
    """
    try:
        if str(val) == 'null' or str(val) == '' or str(val) == [] or str(val) is None or str(val) == 'Null' or str(
                val) == 'NULL':
            return 'N'
        else:
            return str(val)
    except EnvironmentError as err:
        return '发生异常：%s' % err


# 匹配传入的数据并返回第一个匹配结果，未传入的参数默认为空
def val_list(self: str = 'null', user: str = 'null') -> str:
    """
    【匹配传入的数据并返回第一个匹配结果】\n
    :param  self : str 用户组,前后加英文逗号.如：',用户1,用户2,用户3,'；
    :param  user : str 用户,如：用户1 (用户组内包含的部分内容)；
    :return 输出匹配结果；
    """
    try:
        if null(self) == 'N' or null(user) == 'N':
            return '异常：请传入list & user不为空的数据 ...'
        else:
            emp_name = self
            emp_code = user
        bcd = re.search('[,][^,]*' + emp_code + '[^,]*[,]', emp_name, re.M | re.I)  # 对传入的数据进行匹配处理
        if bcd is None:  # 判断匹配的结果
            return '未匹配到对应结果，None'
        val = bcd.group()
        new_name = val[1:-1]  # 截取匹配的结果内容
        return new_name
    except EnvironmentError as err:
        return '发生异常：%s' % err
