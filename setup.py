#!/usr/bin/env python

from setuptools import setup

setup(name='glacierscse',

      version='1.0',

      url='https://github.com/glacierscse/cs207ddl',

      license='MIT',

      author='glacierscse',

      author_email='yifan_wang@g.harvard.edu',

      description='Project for CS 207',

      long_description=open('README.md').read(),

      zip_safe=False,

      setup_requires=['portalocker', 'flask_sqlalchemy']
)