#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import algolia

setup(
    name='django-algolia',
    version=algolia.__version__,
    description='Synchronize your models with the Algolia API for easier and faster searches',
    url='https://github.com/Kmaschta/django-algolia',
    license='BSD',

    packages=find_packages(),
    install_requires=[
        'Django == 1.6',
        'algoliasearch >= 1.5.2',
    ],

    author='Kmaschta',
    author_email='kmaschta@gmail.com',

    include_package_data=False,
    zip_safe=False,
    package_data={
        '': ['README.md', 'LICENSE', 'requirements.txt'],
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
