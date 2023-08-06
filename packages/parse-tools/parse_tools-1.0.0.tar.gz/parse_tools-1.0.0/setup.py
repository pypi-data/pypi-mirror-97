#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
########################################################################

from setuptools import setup
setup(
    name='parse_tools', 
    version='1.0.0', 
    description='A stream performance data parse tools for PyPI', 
    author='dushuangshuang', 
    author_email='shuang2du@163.com', 
    url='https://www.python.org/', 
    license='MIT', 
    keywords='POPpin008366', 
    project_urls={ 
        'Documentation': 'https://packaging.python.org', 
        'Funding': 'https://donate.pypi.org', 
        'Source': 'https://github.com', 
        'Tracker': 'https://github.com',
    }, 
    packages=['parse_tools'], 
    install_requires=['numpy>=1.14', 'tensorflow>=1.7'], 
    python_requires='>=3' 
)
