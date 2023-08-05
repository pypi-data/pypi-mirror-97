#!/usr/bin/env python
#
# Copyright (C) 2020-2021 Ryan Galloway (ryan@rsg.io)
#

import os
import sys
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='subfork',
    version='0.1.0',
    description='Subfork Python API',
    long_description=read('README.rst'),
    author='Ryan Galloway',
    author_email='ryan@rsg.io',
    scripts = ['bin/subfork'],
    packages=find_packages(),
    zip_safe=False
)
