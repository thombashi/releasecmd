# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path

import setuptools


MODULE_NAME = "releasecmd"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}


with io.open(os.path.join(MODULE_NAME, "__version__.py"), encoding=ENCODING) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as f:
    LONG_DESCRIPTION = f.read()

with open(os.path.join(REQUIREMENT_DIR, "build_requirements.txt")) as f:
    BUILD_REQUIRES = [line.strip() for line in f if line.strip()]

SETUPTOOLS_REQUIRES = ["setuptools>=20.2.2"]

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description="Release command for setuptools.setup",
    include_package_data=True,
    keywords=[""],
    license=pkg_info["__license__"],
    long_description=LONG_DESCRIPTION,
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Tracker": "{:s}/issues".format(REPOSITORY_URL),
    },

    install_requires=SETUPTOOLS_REQUIRES,
    setup_requires=SETUPTOOLS_REQUIRES,
    extras_require={
        "build": BUILD_REQUIRES,
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
