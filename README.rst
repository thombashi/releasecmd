releasecmd
============================================
Release command for ``setuptools.setup``. ``ReleaseCommand`` does the following:

1. create a git tag from version information in __version__.py
2. push git tags
3. upload package files to PyPI by using ``twine``

Dependencies
============
- `twine <https://twine.readthedocs.io/>`__
