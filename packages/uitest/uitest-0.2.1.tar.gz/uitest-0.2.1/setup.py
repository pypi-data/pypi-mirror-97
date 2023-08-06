#!/usr/bin/env python

from distutils.core import setup

setup(
    name='uitest',
    version='0.2.1',
    packages=['uitest'],
    url='https://github.com/lizonezhi/uitest.git',
    license='1.0',
    author='lzz',
    author_email='136313283@qq.com',
    description='操作安卓和windows的工具包',
	install_requires=[
        'rsa',
        'psutil',
        'pillow',
        'numpy',
    ]
)
