# encoding: utf-8
"""
    @Time   : 2021-03-08 16:47
    @Author : feikong
"""

import codecs
import os

try:
    from setuptools import setup
except BaseException:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "guandu"
PACKAGES = ['db_cmd']
REQUIRES = []
DESCRIPTION = "base code for project"
LONG_DESCRIPTION = ""
KEYWORDS = "keyword"
AUTHOR = "feikong"
AUTHOR_EMAIL = "feikong@shouxin168.com"
URL = "http://test.com"
VERSION = "1.0.0"
LICENSE = "MIT"
setup(
    name=NAME, version=VERSION,
    description=DESCRIPTION, long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS, author=AUTHOR,
    install_requires=REQUIRES,  # 第三方库依赖
    author_email=AUTHOR_EMAIL, url=URL,
    packages=PACKAGES, include_package_data=True, zip_safe=True,
    entry_points={
        "console_scripts": [
            "wenyali_console = package1.index:index",
        ]
    },
)
