|PyPI Version| |Build Status| |Lint Status| |Coverage Status| |Python Version|

This Python package eases access to information about extensions in the `Open Contracting Data Standard <https://standard.open-contracting.org>`__'s `extension registry <https://github.com/open-contracting/extension_registry>`__.

It includes Python classes for programmatic access, as well as a suite of command-line tools which can:

* download any versions of extensions
* generate POT files (message catalogs) from extension files, as part of a translation worlflow
* generate a data file in JSON format, that provides all the information about versions of extensions

The basic package includes only the Python classes for programmatic access:

.. code-block:: bash

    pip install ocdsextensionregistry

To install the command-line tools, `follow these instructions <https://ocdsextensionregistry.readthedocs.io/en/latest/cli.html>`__.

If you are viewing this on GitHub or PyPi, open the `full documentation <https://ocdsextensionregistry.readthedocs.io/>`__ for additional details.

.. |PyPI Version| image:: https://img.shields.io/pypi/v/ocdsextensionregistry.svg
   :target: https://pypi.org/project/ocdsextensionregistry/
.. |Build Status| image:: https://github.com/open-contracting/extension_registry.py/workflows/CI/badge.svg
.. |Lint Status| image:: https://github.com/open-contracting/extension_registry.py/workflows/Lint/badge.svg
.. |Coverage Status| image:: https://coveralls.io/repos/github/open-contracting/extension_registry.py/badge.svg?branch=main
   :target: https://coveralls.io/github/open-contracting/extension_registry.py?branch=main
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ocdsextensionregistry.svg
   :target: https://pypi.org/project/ocdsextensionregistry/
