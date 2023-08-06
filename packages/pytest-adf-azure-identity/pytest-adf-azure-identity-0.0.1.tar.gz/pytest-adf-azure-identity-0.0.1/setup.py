#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages

version = "0.0.1"


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-adf-azure-identity',
    version=version,
    author='Raki Rahman',
    author_email='mdrakiburrahman@gmail.com',
    maintainer='Raki Rahman',
    maintainer_email='mdrakiburrahman@gmail.com',
    license='MIT',
    url='https://github.com/mdrakiburrahman/pytest-adf-azure-identity',
    description='Pytest plugin for writing Azure Data Factory integration tests',
    # long_description=read('README.rst'),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'adf = pytest_adf.pytest_adf',
        ],
    },
)
