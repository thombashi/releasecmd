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


def get_release_command_class():
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as f:
    LONG_DESCRIPTION = f.read()

SETUPTOOLS_REQUIRES = ["setuptools>=38.3.0"]

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=(
        "releasecmd is a release subcommand for setup.py (setuptools.setup)."
        " the subcommand create a git tag and push, and upload packages to PyPI."
    ),
    include_package_data=True,
    keywords=["release", "setuptools"],
    license=pkg_info["__license__"],
    long_description=LONG_DESCRIPTION,
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Source": REPOSITORY_URL,
        "Tracker": "{:s}/issues".format(REPOSITORY_URL),
    },

    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=SETUPTOOLS_REQUIRES + ["twine"],
    setup_requires=SETUPTOOLS_REQUIRES,
    extras_require={
        "build": ["twine", "wheel"],
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    cmdclass=get_release_command_class())
