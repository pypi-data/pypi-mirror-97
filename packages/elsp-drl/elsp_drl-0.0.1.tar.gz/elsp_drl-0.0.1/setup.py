#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io

from setuptools import setup, find_packages

#############################################
# File Name: setup.py
# Author: Meeea-914
# Mail: 1028634300@qq.com
# Created Time: 2020-12-6 9:05:34
#############################################
VERSION = '0.0.1'
with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()
install_requires = open("requirements.txt").readlines()

setup(
    name="elsp_drl",
    version=VERSION,
    keywords=["pip", "elsp", 'drl'],
    description="elsp drl",
    long_description=long_description,
    license="MIT Licence",

    url="https://github.com/Meeea-914/elsp_drl",
    author="Meeea-914",
    author_email="1028634300@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires,
)
