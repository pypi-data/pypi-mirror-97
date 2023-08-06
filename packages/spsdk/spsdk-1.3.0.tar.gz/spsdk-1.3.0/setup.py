#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2019-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys
from typing import List

import pip  # type: ignore

from setuptools import setup, find_packages  # type: ignore


def sanitize_version(version_str: str) -> str:
    """Change the version into string relevant for comparison."""
    sanitizer = {
        4: version_str + '.0',
        5: '0' + version_str,
        6: version_str
    }
    return sanitizer[len(version_str)]


if sys.version_info >= (3, 8, 0) and sanitize_version(pip.__version__) < '19.2.3':
    print(f"With python {sys.version}, you're using an old version of pip: {pip.__version__}")
    print("Please update pip using: 'python -m pip install --upgrade pip'.")
    sys.exit(1)


with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()
    # avoid build errors on readthedocs (excluding hidapi, which depends on C module)
    if os.getenv('READTHEDOCS'):
        requirements = [x for x in requirements if "hidapi" not in x]
    

with open("README.md", "r") as f:
    long_description = f.read()

# extract version info indirectly
version_info = {}
base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "spsdk", "__version__.py")) as f:
    exec(f.read(), version_info)

setup(
    name='spsdk',
    version=version_info["__version__"],
    description='Open Source Secure Provisioning SDK for NXP MCU/MPU',
    url="https://github.com/NXPmicro/spsdk",
    author="NXP",
    author_email="michal.starecek@nxp.com",
    license='BSD-3-Clause',
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms="Windows, Linux, Mac OSX",
    python_requires=">=3.6",
    setup_requires=[
        'setuptools>=40.0'
    ],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware',
        'Topic :: Utilities'
    ],
    packages=find_packages(exclude=["tests.*", "tests", "examples"]),
    entry_points={
        'console_scripts': [
            'elftosb=spsdk.apps.elftosb:safe_main',
            'pfr=spsdk.apps.pfr:safe_main',
            'pfrc=spsdk.apps.pfrc:safe_main',
            'blhost=spsdk.apps.blhost:safe_main',
            'sdphost=spsdk.apps.sdphost:safe_main',
            'sdpshost=spsdk.apps.sdpshost:safe_main',
            'spsdk=spsdk.apps.spsdk_apps:safe_main',
            'nxpkeygen=spsdk.apps.nxpkeygen:safe_main',
            'nxpdebugmbox=spsdk.apps.nxpdebugmbox:safe_main',
            'nxpcertgen=spsdk.apps.nxpcertgen:safe_main',
            'nxpdevscan=spsdk.apps.nxpdevscan:safe_main',
            'shadowregs=spsdk.apps.shadowregs:safe_main'
        ],
    },
)
