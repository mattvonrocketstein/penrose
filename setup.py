#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

PACKAGE_NAME = 'penrose'
REQUIREMENTS = [
    # also using requirements.txt
    'autopep8', 'flake8',
    'termcolor',
    'pyyaml',
    'click==6.6',
    'repoze.lru == 0.7',
]
setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    author="mvr",
    description="",
    author_email='',
    url='https://github.com/mattvonrocketstein/penrose',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':
        [
            'penrose = {}.bin.main:entry'.format(PACKAGE_NAME),
        ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
