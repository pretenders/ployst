#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

__version__ = '0.1.0'


setup(
    name='ployst',
    version=__version__,
    description='Watch your stories unfold',
    # long_description=open('README.rst').read(),
    author='Carles Barrobés, Alex Couper',
    author_email='carles@barrobes.com, amcouper@gmail.com',
    url='https://github.com/pretenders/ployst',
    packages=find_packages(),
    # install_requires=['django', 'argparse'],
    classifiers=[
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU Library or Lesser General Public License (LGPL)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
)
