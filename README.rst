releasecmd
============================================
.. image:: https://badge.fury.io/py/releasecmd.svg
    :target: https://badge.fury.io/py/releasecmd
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/releasecmd.svg
    :target: https://pypi.org/project/releasecmd
    :alt: Supported Python versions

.. image:: https://github.com/thombashi/releasecmd/actions/workflows/lint.yml/badge.svg
    :target: https://github.com/thombashi/releasecmd/actions/workflows/lint.yml
    :alt: Lint result

Summary
---------
``releasecmd`` is a ``release`` subcommand for ``setup.py`` (``setuptools.setup``).
The subcommand creates a git tag and pushes and uploads packages to ``PyPI``.

The subcommand class (``releasecmd.ReleaseCommand``) is implemented as a subclass of ``setuptools.Command`` class.
The ``release`` subcommand will do the followings:

1. Find a file that defined the package version (``__version__`` variable)
2. Create ``.asc`` (ASCII-armored signature) files of the package binary files if ``--sign`` option is specified
    - https://www.gnupg.org/gph/en/manual/x135.html
3. Create a git tag from the package version information
    - GPG signing to the git tag if ``--sign`` option is specified
4. Push git tags
5. Upload package files to PyPI by using ``twine``
    - uploading for both the package binaries and ``.asc`` files

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


Example
============================================
.. code-block::

    $ python3 setup.py release
    running release
    [get the version from ./releasecmd/__version__.py]
    [pull git tags]
    Already up to date.
    [check existing git tags]
    [create a git tag: v0.0.15]
    [push git tags]
    [upload the package to PyPI]
    ...

prerequisite: package binaries must be in the ``dist/`` directory.


Specify version manually
------------------------------------------------------
You can specify a version manually by ``--version`` option:

.. code-block::

    $ python3 setup.py release --version 0.1.0
    [create a git tag: v0.1.0]
    [pull git tags]
    Already up to date.
    [check existing git tags]
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
    [pull git tags]
    Already up to date.
    [check existing git tags]
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
    skip git tagging
    [upload packages to PyPI]
    ...


release command options
============================================
::

    Options for 'ReleaseCommand' command:
      --skip-tagging    skip a git tag creation
      --skip-uploading  skip uploading packages to PyPI
      --dry-run         do no harm
      --sign            [deprecated from PyPI] make a GPG-signed tag
      --verbose         show verbose output
      --search-dir      specify a root directory path to search a version file.
                        defaults to the current directory.
      --tag-template    specify git tag format. defaults to 'v{version}'.
      --version         specify version manually


Dependencies
============================================
- Python 3.7+
- `Git <https://git-scm.com/>`__
