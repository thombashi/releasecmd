releasecmd
============================================

|PyPI pkg ver| |Supported Python versions| |CI status| |CodeQL|

.. |PyPI pkg ver| image:: https://badge.fury.io/py/releasecmd.svg
    :target: https://badge.fury.io/py/releasecmd
    :alt: PyPI package version

.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/releasecmd.svg
    :target: https://pypi.org/project/releasecmd
    :alt: Supported Python versions

.. |CI status| image:: https://github.com/thombashi/releasecmd/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/releasecmd/actions/workflows/ci.yml
    :alt: CI status

.. |CodeQL| image:: https://github.com/thombashi/releasecmd/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/thombashi/releasecmd/actions/workflows/github-code-scanning/codeql
    :alt: CodeQL

Summary
---------
``releasecmd`` is a ``release`` subcommand for ``setup.py`` (``setuptools.setup``).
The subcommand creates a git tag and pushes and uploads packages to ``PyPI``.

The subcommand class (``releasecmd.ReleaseCommand``) is implemented as a subclass of ``setuptools.Command`` class.
The ``release`` subcommand performs the following tasks:

1. Detect the package version
    1. If specified with the ``--version`` option, use that version
    2. Retrieve the package version from an installed package if the ``--use-installed-version`` option is specified
    3. Find a file that defines the package version (``__version__`` variable)
2. Creates a git tag using the package version information
    - Optionally signs the git tag with GPG if the ``--sign`` option is specified
3. Pushes the git tag
4. Upload package files to PyPI using ``twine``.
 
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
      --skip-tagging           skip a git tag creation
      --skip-uploading         skip uploading packages to PyPI
      --dry-run                don't actually do anything
      --sign                   make a GPG-signed git tag
      --verbose                show verbose output
      --search-dir             specify a root directory path to search a version
                               file. defaults to the current directory.
      --tag-template           specify git tag format. defaults to 'v{version}'
      --use-installed-version  use an installed package version as a release
                               version
      --version                specify release version

Dependencies
============================================
- Python 3.8+
- `Git <https://git-scm.com/>`__
