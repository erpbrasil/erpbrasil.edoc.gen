========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/erpbrail.edoc.gen/badge/?style=flat
    :target: https://readthedocs.org/projects/erpbrailedocgen
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/mileo/erpbrail.edoc.gen.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/mileo/erpbrail.edoc.gen

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/mileo/erpbrail.edoc.gen?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/mileo/erpbrail.edoc.gen

.. |requires| image:: https://requires.io/github/mileo/erpbrail.edoc.gen/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/mileo/erpbrail.edoc.gen/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/mileo/erpbrail.edoc.gen/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/mileo/erpbrail.edoc.gen

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.edoc.gen.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/erpbrasil.edoc.gen

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.edoc.gen.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.edoc.gen

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.edoc.gen.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.edoc.gen

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.edoc.gen.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.edoc.gen

.. |commits-since| image:: https://img.shields.io/github/commits-since/mileo/erpbrail.edoc.gen/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mileo/erpbrail.edoc.gen/compare/v0.1.0...master



.. end-badges

Generate Brazil Edoc with GenerateDS

* Free software: MIT license

Installation
============

::

    pip install erpbrasil.edoc.gen

You can also install the in-development version with::

    pip install https://github.com/mileo/erpbrail.edoc.gen/archive/master.zip


Documentation
=============


https://erpbrailedocgen.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
