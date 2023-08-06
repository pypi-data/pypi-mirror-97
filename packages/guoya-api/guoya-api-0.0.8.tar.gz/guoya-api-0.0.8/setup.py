# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/15 10:46
# !/usr/bin/python

from setuptools import setup

setup(
    name="guoya-api",  # 这里是pip项目发布的名称
    version="0.0.8",  # 版本号，数值大的会优先被pip
    keywords=["init", "auto-api-test"],
    description="果芽API依赖包",
    long_description="果芽软件API自动化依赖包和脚手架脚本",
    license="MIT Licence",

    url="https://gitee.com/guoyasoft/guoya-api.git",  # 项目相关文件地址，一般是github
    author="wuling",
    author_email="wuling@guoyasoft.com",
    # data_files =['init_tool.py'],
    # packages=['tools'],
    platforms="python",
    install_requires=[
        'Faker==6.5.0', # 随机生成仿真数据
        'pinyin==0.4.0',  # 中文转拼音
        'PyMySQL==0.9.3',  # mysql数据库操作
        'xlrd==1.2.0',  # excel读取
        'xlwt==1.3.0',  # excel写入
        'pyyaml==5.1.2',  # yaml文件操作
        'allure-pytest==2.7.0',  # 测试报告框架
        'pytest==5.0.1',  # 单元测试框架
        'requests==2.22.0',# http接口测试框架
        'python-dateutil==2.8.0'  # 时间工具
    ]
)