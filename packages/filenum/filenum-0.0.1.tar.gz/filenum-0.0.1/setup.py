#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="filenum",
    version="0.0.1",
    author="Chen chuan",
    author_email="chenc224@163.com",
    description="file number in directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
#   url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=["filenum/filenum"],
)
