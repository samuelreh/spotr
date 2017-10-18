#!/usr/bin/env python
import codecs
import os.path
import re
import sys
from setuptools import find_packages, setup
from spotr import version

setup(
    name = 'spotr',
    version = version.VERSION,
    description = '',
    long_description=open('README.rst').read(),
    url = 'https://github.com/samuelreh/spotr',
    author = 'Samuel Reh',
    author_email = 'samuelreh@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'boto3'],
    test_require=['coverage', 'pytest', 'pytest-cov', 'mock'],
    entry_points = {
        'console_scripts': [
            'spotr=spotr.spotr:main',
        ],
    },
)
