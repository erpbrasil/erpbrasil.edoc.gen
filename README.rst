========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://api.travis-ci.org/erpbrasil/erpbrasil.edoc.gen.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/erpbrasil/erpbrasil.edoc.gen

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/erpbrasil/erpbrasil.edoc.gen?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/erpbrasil/erpbrasil.edoc.gen

.. |requires| image:: https://requires.io/github/erpbrasil/erpbrasil.edoc.gen/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/erpbrasil/erpbrasil.edoc.gen/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/erpbrasil/erpbrasil.edoc.gen/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.edoc.gen

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.edoc.gen/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.edoc.gen/compare/v0.1.0...master



.. end-badges


Overview
========

This is a helper script for generating Python and Odoo ERP libraries for the Brazilian electronic fiscal documents using http://www.davekuhlman.org/generateDS.html. It supports all fiscal documents that have XSD schemas, that is: NF-e, CC-e, NFS-e, MDF-e, CT-e, EFD-Reinf, e-Social, GNRE, BP-e...

But why a helper instead of launching generateDS manually?

*  For all these fiscal documents there is a common pattern: the schemas are inside a zip archive that can be downloaded from an official URL.
*  After normalizing the xsd file names, we launch the generateDS.py generator on them. But we also want to keep our libraries small, so edoc-gen enables to specify that only some xsd files should support both export and import.
*  Finally automating all the steps with the proper settings allowed Raphaël (`AKRETION <https://akretion.com/pt-BR>`__) to quickly re-generate the Python libraries for all the fiscal documents and run the pytests import/export tests on them to ensure any patch in generateDS would would retain real life compatibility (He got some 6 patches merged into generateDS). And mostly it allowed him to the do the same with the Odoo mixin generator plugin: quicky re-generate all Odoo modules and ensure they install and pass the tests. The libraries and Odoo modules are typically distributed as separated packages inside different repos that can get their own bug reports, forks and contributions but it also work to generate everything in the same directory for a quick extensive testing. Automating all these steps allowed Raphaël to prove to the other Odoo OCA Brazilian localization leaders that we could finally abandon hand written XML fiscal libs such as Pysped who were a hassle to maintain for every fiscal schema and its updates.

This tool was first implemented in Bash by Raphaël Valyi (`AKRETION <https://akretion.com/pt-BR>`__) in 2019 https://github.com/akretion/edoc-gen and then transcoded to Python by (`KMEE <http://www.kmee.com.br/>`__) one year later for an easier portability. It was then cleaned up again by Raphaël to work with the standard generateDS package.

Usage
=====

.. code-block:: html

        erpbrasil.edoc.gen.download_schema --help
        Usage: download_schema.py [OPTIONS]

          Download a list of schemas of the same service, extract it in order and
          overwrite the files.

          NFE: Has one big file with all the xsd and some small files with     new
          fixes named "Pacote de Liberação"

        Options:
          -n, --service_name TEXT  Service Name
          -v, --version TEXT       Version Name
          -u, --url TEXT           List of URLs
          -t DIRECTORY             Directory where the files will be extract
          --help                   Show this message and exit.


        erpbrasil.edoc.gen.generate_python --help
        Usage: generate_python.py [OPTIONS]

          Create a module in the path dest_dir and generates the python lib for each
          xsd found in the path schema_dir

          :param service_name: for example nfe :param version: v4.00 :param
          schema_dir: /tmp/schemas :param force: flag :param dest_dir:
          /tmp/generated_specs :return:

        Options:
          -n, --service_name TEXT   Service Name
          -v, --version TEXT        Version Name
          -s, --schema_dir TEXT     Schema dir
          -f, --force               force
          -d, --dest_dir DIRECTORY  Directory where the files will be extract
          -i, --file_filter TEXT    File Filter
          -m, --main-package TEXT   Main package
          --help                    Show this message and exit.

* Free software: MIT license


Example for the Brazilian NFe
=============================

https://github.com/erpbrasil/nfelib

Example for the NFS-e GINFES

https://github.com/erpbrasil/nfselib/blob/master/scripts/ginfes.sh


Installation
============

::

    pip install erpbrasil.edoc.gen

You can also install the in-development version with::

    pip install https://github.com/erpbrasil/erpbrasil.edoc.gen/archive/master.zip


Credits
=======

Authors / Maintainers:

- Raphaël Valyi (`AKRETION <https://akretion.com/pt-BR>`__)
- Luis Felipe Miléo (`KMEE <http://www.kmee.com.br/>`__)
- Gabriel Cardoso de Faria (`KMEE <http://www.kmee.com.br/>`__)


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
