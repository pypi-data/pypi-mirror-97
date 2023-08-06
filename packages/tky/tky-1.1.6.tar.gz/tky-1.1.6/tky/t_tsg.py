# _*_ coding:utf-8 _*_
"""
常用随机数据生成类集合
\n 目前支持的有：
\n test_msg (tst_email/tst_val/tst_num/tst_one) 随机数据生成（依赖string/random）
\n @author: 'TangKaiYue'
"""

import string
import random


# 随机数据生成
class test_msg:
    """
    【随机数据生成类集合】
    \n 目前支持的有：
    \n tst_email | 邮箱随机生成（依赖string/random）
    \n tst_val | 传入文本随机生成（依赖random）
    \n tst_num | 数字随机生成（依赖random）
    \n tst_one | 随机取一个传入的值（依赖random）
    """

    # 邮箱随机生成
    def tst_email(self=['.com', '.cn', '.org', '.net'], n_min: int = 6, n_max: int = 12, z_min: int = 2, z_max: int = 5,
                  other: str = ''):
        """
        【邮箱随机生成】（依赖string/random）\n
        :param self: 邮箱后缀,默认：['.com', '.cn', '.org', '.net']；
        :param n_min: 邮箱名称最小位数,默认：6；
        :param n_max: 邮箱名称最大位数,默认：12,须大于最小位数；
        :param z_min: 邮箱后缀最小位数,默认：2；
        :param z_max: 邮箱后缀最大位数,默认：5,须大于最小位数；
        :param other: 名称里添加加其他符号；
        :return: 生成的邮箱；
        """
        try:
            # 常用邮箱后缀
            characters = string.ascii_uppercase + string.digits + str(other)  # 拼接大写+数字 的邮箱前称
            characters1 = string.ascii_lowercase + string.digits  # 拼接小写+数字 邮箱服务商名称
            # 字母数字集合
            username = ''.join((random.choice(characters) for i in range(random.randint(n_min, n_max))))
            # 6-12的随机整数用户名
            domain = ''.join((random.choice(characters1) for i in range(random.randint(z_min, z_max))))
            return username + '@' + domain + random.choice(self)
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 传入文本随机生成
    def tst_val(self: str = ('男', '女'), z_min: int = 1, z_max: int = 1):
        """
        【传入文本随机生成】（依赖random）\n
        :param self: 要生成的内容，默认为：('男', '女')；
        :param z_min: 文本最小位数,默认：1；
        :param z_max: 文本最大位数,默认：1,须大于最小位数；
        :return:  输出随机生成的结果
        """
        try:
            val = ''.join((random.choice(self) for i in range(random.randint(z_min, z_max))))
            return val
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 数字随机生成
    def tst_num(self: str = '', z_min: int = 0, z_max: int = 9, num: int = 10):
        """
        【数字随机生成】（依赖random）\n
        :param self: 数字串首个数字,默认为空；
        :param z_min: 数字最小位数,默认：0(建议0-9)；
        :param z_max: 数字最大位数,默认：9(建议0-9),须大于最小位数；
        :param num: 生成多少位数字,默认：10(有首字/大小多位时需排除算)；
        :return:  输出随机生成的结果(受最小最大多位数影响)
        """
        try:
            val = str(self) + ''.join((str(random.randint(z_min, z_max)) for i in range(num)))
            return val
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 随机取一个传入的值
    def tst_one(self: str = ('北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省',
                             '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省',
                             '台湾省', '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区')):
        """
        【随机取一个传入的值】（依赖random）\n
        :param self: 传入的文本,默认为省份数据；
        :return:  输出随机生成的结果
        """
        try:
            val = random.choice(self)
            return val
        except EnvironmentError as err:
            return '发生异常：%s' % err
