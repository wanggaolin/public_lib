#!/usr/bin/env python
#encoding=utf-8
import setuptools
from public_lib import _version
setuptools.setup(
    name='public_lib',
    version=_version,
    description="python public lib for me",
    classifiers=[],
    author='GaoLin',
    author_email='brach@lssin.com',
    url='https://github.com/wanggaolin/public_lib',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['tests']),
    keywords = ['public','lib'],
    install_requires = [
        'python>=2.7',
        'psutil',
    ]
)