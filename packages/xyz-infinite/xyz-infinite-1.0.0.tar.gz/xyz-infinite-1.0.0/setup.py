# -*- coding:utf-8 -*-
from __future__ import print_function

from setuptools import setup, find_packages

setup(
    name="xyz-infinite",
    version="1.0.0",
    keywords='wx',
    description='a library for save your time',
    license='MIT License',
    url='https://github.com/wxnacy/wwx',
    author='changping',
    author_email='xiaoyao_cp@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        "huepy==1.2.1",
    ],
    zip_safe=True,
)
