# -*- coding: utf-8 -*-
# @Time    : 2020/10/28-13:48
# @Author  : 吕玮嘉    1936094276@qq.com
# @File    : setup.py
# @Software: win10  python3.6 PyCharm
import setuptools
with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="125softNLP",
    version="0.0.1",
    author="lvweijia",
    author_email="1936094276@qq.com",
    description="Python wrapper for pysoftNLP: Natural language processing project of 863 Software Incubator Co., Ltd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tensorflow', #1.14.0
    ],
)


