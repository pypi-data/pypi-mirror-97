#!/usr/bin/env python
"""
Mapilio Helper
"""
from __future__ import (absolute_import, division, print_function)

import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 5):
    raise RuntimeError(
        "Mapilio Helper tools supports Python 3.6 and above. "
    )

# This import must be below the above `sys.version_info` check,
# because the code being imported here is not compatible with the older
# versions of Python.
from helper.util import __version__ as version # noqa

INSTALL_REQUIRES = [
    'trianglesolver==1.2',
    'opencv-python==4.5.1.48'
]

setup(
    name='helper-mapilio',
    version=version,
    description='Mapilio Helper Library',
    url='https://github.com/mapilio/helper.git',
    author='Mapilio - Ozcan Durak & M.Can VARER',
    author_email='ozcan@visiosoft.com.tr',
    license='licensed',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6, <4",
    project_urls={  # Optional
            'Bug Reports': 'https://github.com/mapilio/helper/issues',
            'Say Thanks!': 'https://mapilio.com/#contact',
            'Source': 'https://github.com/mapilio/helper/',
        },
)