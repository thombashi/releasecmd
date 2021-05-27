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
The ``release`` subcommand will do the followings:

1. Find a file that defined the package version (e.g. ``<package>/__init__.py``)
2. Create ``.asc`` files if ``--sign`` option is specified
3. Create a git tag from the package version information
    - GPG signing to the git tag if ``--sign`` option is specified
4. Push git tags
5. Upload package files to PyPI by using ``twine``


Installation
============================================
::

    pip install releasecmd


Usage
============================================

:setup.py:
    .. code-block:: python

        import setuptools

        from releasecmd import ReleaseCommand

        setuptools.setup(
            ...
            cmdclass={"release": ReleaseCommand},
        )


release command options
============================================
::

    Options for 'ReleaseCommand' command:
      --skip-tagging  skip a git tag creation
      --dry-run       do no harm
      --sign          make a GPG-signed tag
      --search-dir    specify a root directory path to search a version file.
                      defaults to the current directory.
      --tag-template  specify git tag format. defaults to 'v{version}'.
      --version       specify version manually


Example
============================================
.. code-block::

    $ python3 setup.py release
    running release
    [get the version from ./releasecmd/__version__.py]
    [create a git tag: v0.0.15]
    [push git tags]
    [upload the package to PyPI]
    ...

prerequisite: package binaries must bein in the ``dist/`` directory.


Specify version manually
------------------------------------------------------
You can specify a vesion manually by ``--version`` option:

.. code-block::

    $ python3 setup.py release --version 0.1.0
    [create a git tag: v0.1.0]
    [push git tags]
    [upload packages to PyPI]


Create a GPG signed tag and upload packages
------------------------------------------------------
.. code-block::

    $ python3 setup.py release --sign
    running release
    [get the version from ./releasecmd/__version__.py]
    [create a .asc file for releasecmd-0.1.0.tar.gz]
    [create a .asc file for releasecmd-0.1.0-py2.py3-none-any.whl]
    [create a git tag with gpg signing: v0.1.0]
    [push git tags]
    [upload packages to PyPI]
    ...

Skip create a git tag and upload packages
------------------------------------------------------
.. code-block::

    $ python3 setup.py release --skip-tagging
    running release
    [get the version from ./releasecmd/__version__.py]
    [push git tags]
    [upload packages to PyPI]
    ...


Dependencies
============================================
- Python 3.5+
- `Git <https://git-scm.com/>`__
