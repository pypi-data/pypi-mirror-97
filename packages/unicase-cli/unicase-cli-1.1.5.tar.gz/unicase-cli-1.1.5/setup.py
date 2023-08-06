#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2021/2/21 18:41
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="unicase-cli",
    version="1.1.5",
    author="mocobk",
    author_email="mailmzb@qq.com",
    description="manage Excel cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="unicase-cli,unicase,case,excel",
    url="https://github.com/mocobk/unicase",
    packages=['unicase'],
    install_requires=['click', 'jinja2', 'requests', 'openpyxl', 'terminal-layout'],
    entry_points={"console_scripts": ["unicase = unicase.cli:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'unicase': ['template/*']},
)