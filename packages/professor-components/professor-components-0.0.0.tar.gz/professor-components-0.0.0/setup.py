#!/usr/bin/env python

import os
from setuptools import setup

VERSION = "0.0.0"
NAME = os.environ['NAME']

setup(
    name=NAME,
    version=VERSION,
    description="Dummy package in order to prevent from security issue.",
    author="Mercari",
    zip_safe=False,
    include_package_data=True,
)