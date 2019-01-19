releasecmd
============================================
.. image:: https://badge.fury.io/py/releasecmd.svg
    :target: https://badge.fury.io/py/releasecmd
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/releasecmd.svg
    :target: https://pypi.org/project/releasecmd
    :alt: Supported Python versions

Summary
---------
``releasecmd`` is a ``release`` subcommand for ``setup.py`` (``setuptools.setup``).
The subcommand create a git tag and push, and upload packages to ``PyPI``.

The subcommand class (``releasecmd.ReleaseCommand``) is implemented as
a subclass of ``setuptools.Command`` class.
The ``release`` subcommand does the followings:

1. create a git tag from the package version information
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
    ...

Before execute, need to exist uploading binaries in ``dist/`` directory.

Skip create a git tag
---------------------------
.. code-block::

    $ python setup.py release --skip-tagging
    running release
    ...


Dependencies
============================================
- `twine <https://twine.readthedocs.io/>`__
