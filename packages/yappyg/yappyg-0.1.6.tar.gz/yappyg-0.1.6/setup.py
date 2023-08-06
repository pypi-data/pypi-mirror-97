#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
yappyG is Yet Another Package for Py Git
"""

from setuptools import find_packages, setup

VERSION = '0.1.6'


options = dict(
    name="yappyg",
    version=VERSION,
    description="Yet Another Package for Py Git, that handles user/pass prompts in native python",
    long_description=__doc__,
    author="Lucas Durand",
    author_email="lucas@lucasdurand.xyz",
    license="BSD",
    platforms="Any",
    install_requires=['log_colorizer','nbdime'],
    provides=['yappyg'],
    packages=find_packages(),
    url = 'https://github.com/lucasdurand/yappyG',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"])

setup(**options)
