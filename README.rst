releasecmd
============================================
Release command class (``ReleaseCommand``) for ``setuptools.setup``.
``ReleaseCommand`` does the following:

1. create a git tag from version information in ``__version__.py``
2. push git tags
3. upload package files to PyPI by using ``twine``


Example
============================================
- https://github.com/thombashi/typepy/blob/master/setup.py

.. code-block::

    $ python setup.py release
    [reading ./typepy/__version__.py]
    [pushing git tags: v0.0.26]
    [upload packages to PyPI]


Dependencies
============================================
- `twine <https://twine.readthedocs.io/>`__
