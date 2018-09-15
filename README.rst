releasecmd
============================================
.. image:: https://badge.fury.io/py/releasecmd.svg
    :target: https://badge.fury.io/py/releasecmd

.. image:: https://img.shields.io/pypi/pyversions/releasecmd.svg
   :target: https://pypi.org/project/releasecmd

Summary
---------
``releasecmd`` will add ``release`` subcommand to
``setup.py`` (``setuptools.setup``) by ``releasecmd.ReleaseCommand`` class.
The class is implemented as a subclass of ``setuptools.Command`` class.
The ``release`` subcommand does the following:

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
