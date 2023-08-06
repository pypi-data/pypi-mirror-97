# _*_ coding:utf-8 _*_
"""
常用DEV类集合
\n 目前支持的方法有：
\n app_dev （移动设备连接，依赖appium）
\n pc_dev （浏览器连接，依赖selenium）
\n @author: 'TangKaiYue'
"""

from .t_jde import null


# 移动设备连接
def app_dev(osn: str = 'null', osv: str = 'null', dvn: str = 'null', package: str = 'null', activity: str = 'null',
            cod: str = '5554'):
    """
    【GUI_APP移动设备连接,端口默认为5554】\n
    :param osn: str 设备系统,如：Android；
    :param osv: str 设备系统版本,如：7.1.2；
    :param dvn: str 设备名称,如：device；
    :param package: str 设备APP包名,如：com.xxx.app.addressbook；
    :param activity: str 设备里APP包的启动入口,如：om.xxx.app.addressbook.activity.WelcomeActivity;
    :param cod: str Appium里设置的端口号，默认5554
    :return: 输出driver
    """
    try:
        if null(osn) == 'N' or null(osv) == 'N' or null(dvn) == 'N' or null(package) == 'N' or null(activity) == 'N':
            return print("异常：系统名称、系统版本、设备名称、APP包名、APP包名入口 都不能为空...")
        else:
            from appium import webdriver
            caps = {}
            caps['platformName'] = str(osn)  # 设备系统
            caps['platformVersion'] = str(osv)  # 设备系统版本
            caps['deviceName'] = str(dvn)  # 设备号
            caps['appPackage'] = str(package)  # 设备里APP包名
            caps['appActivity'] = str(activity)  # 设备里APP包的启动入口
            driver = webdriver.Remote('http://localhost:%s/wd/hub' % cod, caps)  # 启动app（端口与Appium里设置的保持一致）
            return driver
    except EnvironmentError as err:
        return '发生异常：%s' % err


# PC浏览器连接
def pc_dev(bro: str = 'g', url: str = 'null'):
    """
    【GUI_PC浏览器连接,默认最大经窗口】\n
    :param bro: str 浏览器,代码支持：g(谷歌),f(火狐)；默认g；
    :param url: str 要打开的URL链接；
    :return: 执行打开浏览器和URL的操作；
    """
    try:
        if null(bro) == 'N' or null(url) == 'N':
            return print("异常：浏览器、URL 都不能为空...")
        else:
            from selenium import webdriver
            if bro == 'g':
                driver = webdriver.Chrome()  # 驱动Chrome浏览器
                driver.maximize_window()  # 窗口最大化
                driver.get(url)  # 打开指定网址
                return driver

            elif bro == 'f':
                driver = webdriver.Firefox()  # 驱动Firefox浏览器
                driver.maximize_window()  # 窗口最大化
                driver.get(url)  # 打开指定网址
                return driver
            else:
                print('启动异常：非常抱歉，暂时只支持：g/f 谷歌/火狐, 使用其他请自行编写方法或联系作者集合...')
    except Exception as one3:
        print('\n捕捉到程序异常：%s' % one3)
