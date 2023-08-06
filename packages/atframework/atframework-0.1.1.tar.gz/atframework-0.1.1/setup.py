from setuptools import setup

setup(
name = 'atframework',
version = '0.1.1',
author = 'Siro',
author_email = 'siro@foxmail.com',
description = 'this is one automation framework base on selenium',
long_description = 'file: README.md',
long_description_content_type = 'text/markdown',
url = 'https://github.com/pypa/sampleproject',
py_modules = ['drivers','tools','web'],
install_requires=['pytest', 'pytest-html','pytest-ordering','pytest-rerunfailures','allure-pytest','pytest-xdist','selenium'],
python_requires='>=3.5'
)