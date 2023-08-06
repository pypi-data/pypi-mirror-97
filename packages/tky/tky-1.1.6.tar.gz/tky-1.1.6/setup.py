# _*_ coding:utf-8 _*_
from setuptools import find_packages, setup

setup(
    name='tky',  # 模块名称
    version='1.1.6',  # 模块版本号
    author='Tang kai yue',  # 作者名
    author_email='tky_1314@163.com',  # 作者邮箱
    maintainer='Tang kai yue',  # 维护者
    maintainer_email='tky_1314@163.com',  # 维护者邮箱
    description='tang kai yue 个人使用python方法集合',  # 模块描述
    long_description_content_type='text/markdown',  # 文档格式
    long_description=open('README.md', 'r', encoding='UTF-8').read(),  # 这里是文档内容, 读取readme文件
    url="https://gitee.com/tangkaiyue/tky",
    packages=find_packages(),
    # install_requires=['xml', 'os', 'urllib'],  # 需要依赖的包
    classifiers=[  # 这里我们指定证书, python版本和系统类型
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3',  # 这里指定python版本号必须大于等于3才可以安装
)
