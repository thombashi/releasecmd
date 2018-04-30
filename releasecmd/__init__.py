# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import print_function, unicode_literals

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
import errno
import io
import os
import re
import subprocess
import sys

import setuptools


_VERSION_FILE_NAME = "__version__.py"


class ReleaseCommand(setuptools.Command):
    description = "create a tag and push, and upload packages to PyPI"

    # command class must provide 'user_options' attribute (a list of tuples)
    user_options = [
        ('dry-run', None, 'do no harm'),
    ]

    __DIST_DIR_NAME = "dist"

    def initialize_options(self):
        self.dry_run = False

    def finalize_options(self):
        pass

    def run(self):
        """
        1. create a git tag from version information in __version__.py
        2. push git tags
        3. upload package files to PyPI by using twine
        """

        self.__validate_dist_dir()

        version = self.__get_version()
        self.__validate_version(version)

        upload_file_list = self.__get_upload_file_list(version)
        if not upload_file_list:
            sys.stderr.write(
                "file not found in '{dir:s}/' that matches version ({version:s}) to upload\n".format(
                    dir=self.__DIST_DIR_NAME, version=version))
            sys.exit(errno.ENOENT)

        self.__push_git_tag(version)
        self.__upload_package(upload_file_list)

    def __validate_dist_dir(self):
        if os.path.isdir(self.__DIST_DIR_NAME):
            return

        sys.stderr.write("directory not found: {:s}/\n".format(self.__DIST_DIR_NAME))
        sys.exit(errno.ENOENT)

    def __validate_version(self, version):
        from pkg_resources import parse_version
        from pkg_resources.extern.packaging.version import Version, LegacyVersion

        if not isinstance(parse_version(version), Version):
            sys.stderr.write("invalid version string: {}\n".format(version))
            sys.exit(errno.EINVAL)

    def __get_version(self):
        pkg_info = {}
        version_file_path = self.__find_version_file()

        if not version_file_path:
            sys.stderr.write("{} not found\n".format(_VERSION_FILE_NAME))
            sys.exit(errno.ENOENT)

        print("[reading {}]".format(version_file_path))

        with io.open(version_file_path, encoding="utf8") as f:
            exec(f.read(), pkg_info)

        return pkg_info["__version__"]

    def __push_git_tag(self, version):
        tag = "v{}".format(version)

        print("[pushing git tags: {}]".format(tag))

        command = "git tag {}".format(tag)
        if self.dry_run:
            print(command)
        else:
            return_code = subprocess.call(command, shell=True)
            if return_code != 0:
                sys.exit(return_code)

        command = "git push --tags"
        if self.dry_run:
            print(command)
        else:
            return_code = subprocess.call(command, shell=True)
            if return_code != 0:
                sys.exit(return_code)

    def __get_upload_file_list(self, version):
        version_regexp = re.compile(re.escape(version))
        upload_file_list = []

        for filename in os.listdir(self.__DIST_DIR_NAME):
            if not version_regexp.search(filename):
                continue

            upload_file_list.append(os.path.join(self.__DIST_DIR_NAME, filename))

        return upload_file_list

    def __upload_package(self, upload_file_list):
        print("[upload packages to PyPI]")
        command = "twine upload {:s}".format(" ".join(upload_file_list))
        if self.dry_run:
            print(command)
        else:
            subprocess.call(command, shell=True)

    @staticmethod
    def __find_version_file():
        exclude_regexp_list = [
            re.compile("/build/.+"),
            re.compile(re.escape("/.eggs/")),
        ]

        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename != _VERSION_FILE_NAME:
                    continue

                if any([regexp.search(root) for regexp in exclude_regexp_list]):
                    continue

                return os.path.join(root, filename)

        return None
