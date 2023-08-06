# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    version = 'v8.7', #版本

    # 依赖包, 如果没有, 可以不要
    # baidu-aip包会报错, 需手动添加
    # 手动安装 scrapy 库
    requires = [
        'pandas', 'pymysql', 'requests', 'numpy', 'sqlalchemy', 'apscheduler'
    ],

    description = 'me', # 简要描述
    py_modules = [], # 需要打包的模块
    packages = ['phk'],
    name = 'phk',# 需要打包的名字, 即本模块要发布的名字
    author = 'jutooy', # 作者名
    author_email = 'jutooy@qq.com',   # 作者邮件
    url='https://www.yuque.com/jutooy/python/', # 项目地址,一般是代码托管的网站
    license = 'MIT'
)

# 步骤:
# 修改版本号
# python 删除旧文件.py
# push到码云
# python setup.py sdist bdist_wheel
# twine upload dist/*
#     账号: 
#     密码: 
# python 删除旧文件.py
# pip install --upgrade phk
