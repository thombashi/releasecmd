releasecmd
============================================
.. image:: https://badge.fury.io/py/releasecmd.svg
    :target: https://badge.fury.io/py/releasecmd
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/releasecmd.svg
    :target: https://pypi.org/project/releasecmd
    :alt: Supported Python versions

.. image:: https://github.com/thombashi/releasecmd/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/releasecmd/actions/workflows/ci.yml
    :alt: Lint result

Summary
---------
``releasecmd`` is a ``release`` subcommand for ``setup.py`` (``setuptools.setup``).
The subcommand creates a git tag and pushes and uploads packages to ``PyPI``.

The subcommand class (``releasecmd.ReleaseCommand``) is implemented as a subclass of ``setuptools.Command`` class.
The ``release`` subcommand will do the followings:

1. Find a file that defined the package version (``__version__`` variable)
2. Create a git tag from the package version information
    - GPG signing to the git tag if ``--sign`` option is specified
3. Push git tags
4. Upload package files to PyPI by using ``twine``
 
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
      --sign            make a GPG-signed git tag
      --verbose         show verbose output
      --search-dir      specify a root directory path to search a version file.
                        defaults to the current directory.
      --tag-template    specify git tag format. defaults to 'v{version}'.
      --version         specify version manually


Dependencies
============================================
- Python 3.8+
- `Git <https://git-scm.com/>`__
