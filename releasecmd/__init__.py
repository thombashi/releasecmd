"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import errno
import os
import re
import subprocess
import sys
from typing import Dict, Generator, List, Optional

import setuptools

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._retry import Retry, sleep_before_retry


class ReleaseCommand(setuptools.Command):
    description = "create a Git tag and push, and then upload packages to PyPI"

    # command class must provide 'user_options' attribute (a list of tuples)
    user_options = [
        ("skip-tagging", None, "skip a git tag creation"),
        ("dry-run", None, "do no harm"),
        ("sign", None, "make a GPG-signed tag"),
        (
            "search-dir=",
            None,
            "specify a root directory path to search a version file. "
            "defaults to the current directory.",
        ),
        ("tag-template=", None, "specify git tag format. defaults to 'v{version}'."),
        ("version=", None, "specify version manually"),
    ]

    __DIST_DIR_NAME = "dist"
    __TAG_ALREADY_EXISTS = 128

    def initialize_options(self) -> None:
        self.skip_tagging = False
        self.dry_run = False
        self.sign = False
        self.search_dir = "."
        self.tag_template = "v{version}"
        self.version = None  # type: Optional[str]

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """
        1. create asc files (if specified --sign option)
        2. create a git tag from version information in __version__.py
        3. push git tags
        4. upload package files to PyPI by using twine
        """

        self.__validate_dist_dir()

        version = self.__get_version()
        self.__validate_version(version)
        self.__sign_package(version)

        upload_file_list = self.__get_upload_files(version)
        if not upload_file_list:
            print(
                (
                    "package files not found in '{dir:s}/' that matches the version ({version:s}) "
                    + "to upload"
                ).format(dir=self.__DIST_DIR_NAME, version=version),
                file=sys.stderr,
            )
            sys.exit(errno.ENOENT)

        self.__create_git_tag(version)
        self.__upload_package(upload_file_list)

    def __validate_dist_dir(self) -> None:
        if os.path.isdir(self.__DIST_DIR_NAME):
            return

        print(
            f"{self.__DIST_DIR_NAME:s}/ directory not found. build the package first.",
            file=sys.stderr,
        )
        sys.exit(errno.ENOENT)

    def __validate_version(self, version: str) -> None:
        from pkg_resources import parse_version
        from pkg_resources.extern.packaging.version import Version

        if not isinstance(parse_version(version), Version):
            print(f"[ERROR] invalid version string: {version}", file=sys.stderr)
            sys.exit(errno.EINVAL)

    def __get_version(self) -> str:
        if self.version:
            return self.version

        for version_file in self.__traverse_version_file():
            version = self.__extract_version_from_file(version_file)

            if version:
                print(f"[get the version from {version_file}]")
                return version

        print(
            f"[ERROR] version not found in the directory '{self.search_dir}'",
            file=sys.stderr,
        )
        sys.exit(errno.ENOENT)

    def __extract_version_from_file(self, filepath: Optional[str]) -> Optional[str]:
        pkg_info = {}  # type: Dict[str, str]

        if not filepath:
            print("require a file path", file=sys.stderr)
            sys.exit(errno.ENOENT)

        if not os.path.isfile(filepath):
            print(f"file not found: {filepath}", file=sys.stderr)
            sys.exit(errno.ENOENT)

        with open(filepath, encoding="utf8") as f:
            try:
                exec(f.read(), pkg_info)
            except KeyError:
                return None

        return pkg_info.get("__version__")

    def __print_error(self, command_str: str, error_msg: str) -> None:
        print(f"[ERROR] {command_str}", file=sys.stderr)
        if error_msg:
            print(error_msg, file=sys.stderr)

    def __call(self, command: List[str], retry: Optional[Retry] = None) -> str:
        command_str = " ".join(command)

        if self.dry_run:
            print(f"dry run: {command_str}")
            return ""

        result = subprocess.run(command, stderr=subprocess.PIPE, encoding="utf8")
        if result.returncode == 0:
            return result.stdout

        if not retry:
            self.__print_error(command_str, error_msg=result.stderr)
            sys.exit(result.returncode)

        for i in range(retry.total):
            self.__print_error(command_str, error_msg=result.stderr)
            sleep_before_retry(attempt=i + 1, retries=retry.total)

            result = subprocess.run(command, stderr=subprocess.PIPE, encoding="utf8")
            if result.returncode == 0 or result.returncode in retry.no_retry_returncodes:
                return result.stdout

        sys.exit(result.returncode)

    def __create_git_tag(self, version: str) -> None:
        tag = self.tag_template.format(version=version)

        if self.skip_tagging:
            print("skip git tagging")
            return

        print("[pull git tags]")
        self.__call(["git", "pull", "--tags"], retry=Retry())

        command_items = ["git", "tag"]  # type: List[str]
        extra_log = ""
        if self.sign:
            command_items.extend(["--sign", "-m", f"'GPG signed {version} tag'"])
            extra_log = " with gpg signing"
        command_items.append(tag)
        print(f"[create a git tag{extra_log}: {tag}]")
        self.__call(command_items)

        print("[push git tags]")
        self.__call(
            ["git", "push", "--tags"], retry=Retry(no_retry_returncodes=[self.__TAG_ALREADY_EXISTS])
        )

    def __get_upload_files(self, version: str) -> List[str]:
        version_regexp = re.compile(fr".+-{re.escape(version):s}.*(\.tar\.gz|\.whl)(\.asc$)?")
        upload_file_list = []  # type: List[str]

        for filename in os.listdir(self.__DIST_DIR_NAME):
            if not version_regexp.search(filename):
                continue

            upload_file_list.append(os.path.join(self.__DIST_DIR_NAME, filename))

        return upload_file_list

    def __sign_package(self, version: str) -> None:
        if not self.sign:
            return

        pkg_regexp = re.compile(fr".+-{re.escape(version):s}.*(\.tar\.gz$|\.whl$)")

        for filename in os.listdir(self.__DIST_DIR_NAME):
            if not pkg_regexp.search(filename):
                continue

            print(f"[create a .asc file for {filename}]")

            self.__call(
                ["gpg", "--detach-sign", "--armor"] + [os.path.join(self.__DIST_DIR_NAME, filename)]
            )

    def __upload_package(self, upload_file_list: List[str]) -> None:
        print("[upload packages to PyPI]")
        self.__call(["twine", "upload"] + upload_file_list, retry=Retry())

    def __traverse_version_file(self) -> Generator[Optional[str], None, None]:
        exclude_regexp_list = [
            re.compile("/build/.+"),
            re.compile(re.escape("/.eggs/")),
            re.compile(re.escape(".tox/")),
        ]
        ver_file_candidate_regexp = re.compile(r"^_.+_\.py$")

        for root, dirs, files in os.walk(self.search_dir):
            for filename in files:
                if ver_file_candidate_regexp.search(filename) is None:
                    continue

                if any([exclude_regexp.search(root) for exclude_regexp in exclude_regexp_list]):
                    continue

                yield os.path.join(root, filename)

        return None
