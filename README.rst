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

1. Find a file that defined the package version
2. Create a git tag from the package version information
3. Push git tags
4. Upload package files to PyPI by using ``twine``


Example
============================================

.. code-block::

    $ python setup.py release
    running release
    [get the version from ./releasecmd/__version__.py]
    [create a git tag: v0.0.15]
    [push git tags]
    [upload the package to PyPI]
    ...

Before execute, need to exist uploading binaries in ``dist/`` directory.

Create a GPG signed tag
---------------------------
.. code-block::

    $ python setup.py release --sign
    running release
    [get the version from ./releasecmd/__version__.py]
    [create a git tag with gpg signing: v0.0.15]
    [push git tags]
    [upload the package to PyPI]
    ...

Skip create a git tag
---------------------------
.. code-block::

    $ python setup.py release --skip-tagging
    running release
    [get the version from ./releasecmd/__version__.py]
    [push git tags]
    [upload the package to PyPI]    
    ...


Dependencies
============================================
- `twine <https://twine.readthedocs.io/>`__
