# -*- coding:utf-8 -*-
from __future__ import print_function

from setuptools import setup, find_packages

setup(
    name="xyz_tibet",
    version="0.2.0",
    keywords='wx',
    description='a library for wx Developer',
    license='MIT License',
    url='https://github.com/wxnacy/wwx',
    author='changping',
    author_email='xiaoyao_cp@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pandas>=0.20.0',  # 所需要包的版本号
        'numpy>=1.14.0',  # 所需要包的版本号
        "huepy==1.2.1",
    ],
    zip_safe=True,
)
