# -*- coding: utf-8 -*-
# @Time     ： 2020/11/12 2:26 下午
# @Author   :  haleli

'''Tencent is pleased to support the open source community by making FAutoTest available. Copyright (C) 2018 THL A29
Limited, a Tencent company. All rights reserved. Licensed under the BSD 3-Clause License (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language governing permissions and limitations
under the License.

'''
from setuptools import setup, find_packages

NAME = "multi-platform"
VERSION = "0.4.4"
AUTHOR = "haleli"
AUTHOR = "pengfeeli"
PACKAGES = find_packages()
CLASSIFIERS = [
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3.6",
]

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    install_requires=[]
)
