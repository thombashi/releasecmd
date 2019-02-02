# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import errno
import io
import os
import re
import subprocess
import sys

import setuptools

from .__version__ import __author__, __copyright__, __email__, __license__, __version__


class ReleaseCommand(setuptools.Command):
    description = "create a Git tag and push, and then upload packages to PyPI"

    # command class must provide 'user_options' attribute (a list of tuples)
    user_options = [
        ("skip-tagging", None, "skip a git tag creation"),
        ("dry-run", None, "do no harm"),
        ("sign", None, "make a GPG-signed tag"),
    ]

    __DIST_DIR_NAME = "dist"

    def initialize_options(self):
        self.skip_tagging = False
        self.dry_run = False
        self.sign = False

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
                    dir=self.__DIST_DIR_NAME, version=version
                )
            )
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
        for version_file in self.__traverse_version_file():
            version = self.__extract_version_from_file(version_file)

            if version:
                return version

        print("version not found in the curent directory", file=sys.stderr)
        sys.exit(errno.ENOENT)

    def __extract_version_from_file(self, filepath):
        pkg_info = {}

        if not filepath:
            print("require a file path", file=sys.stderr)
            sys.exit(errno.ENOENT)

        print("[get the version from {}]".format(filepath))

        with io.open(filepath, encoding="utf8") as f:
            try:
                exec(f.read(), pkg_info)
            except KeyError:
                return None

        return pkg_info.get("__version__")

    def __call(self, command):
        if self.dry_run:
            print("dry run: {}".format(command))
            return

        return_code = subprocess.call(command, shell=True)
        if return_code != 0:
            sys.exit(return_code)

    def __push_git_tag(self, version):
        tag = "v{}".format(version)

        if not self.skip_tagging:
            command_items = ["git", "tag"]
            extra_log = ""

            if self.sign:
                command_items.extend(["--sign", "-m", "'signed {} tag'".format(version)])
                extra_log = " with gpg signing"

            print("[create a git tag{}: {}]".format(extra_log, tag))

            command_items.append(tag)

            self.__call(" ".join(command_items))

        print("[push git tags]")
        self.__call("git push --tags")

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
        self.__call("twine upload {:s}".format(" ".join(upload_file_list)))

    @staticmethod
    def __traverse_version_file():
        exclude_regexp_list = [re.compile("/build/.+"), re.compile(re.escape("/.eggs/"))]
        ver_file_candidate_regexp = re.compile("^__.+__\.py$")

        for root, dirs, files in os.walk("."):
            for filename in files:
                if ver_file_candidate_regexp.search(filename) is None:
                    continue

                if any([exclude_regexp.search(root) for exclude_regexp in exclude_regexp_list]):
                    continue

                yield os.path.join(root, filename)

        return None
