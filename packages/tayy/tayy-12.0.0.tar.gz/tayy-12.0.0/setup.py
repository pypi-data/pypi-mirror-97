#!/usr/bin/env python
#-*- coding:utf-8 -*-
import setuptools

setuptools.setup(
    name="tayy", # Replace with your own username
    version="12.0.0",
    author="wing",
    author_email="100102888@qq.com",
    description="A small example package",
    long_description_content_type="text/markdown",
    url="https://github.com/ladjrong/tayy2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
)
