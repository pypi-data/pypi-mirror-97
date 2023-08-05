Subfork Python API
==================

This package provides the Subfork Python API and command
line interface.

Installation
~~~~~~~~~~~~

The easiest way to install:

::

    $ pip install subfork

Configuration
~~~~~~~~~~~~~

To use environment variables, do the following:

::

    $ export SUBFORK_ACCESS_KEY=MYACCESKEY
    $ export SUBFORK_SECRET_KEY=MYSECRETKEY

To use a shared config file, create a config.yaml
file like this:

::

    SUBFORK_ACCESS_KEY: MYACCESKEY
    SUBFORK_SECRET_KEY: MYSECRETKEY


Basic Commands
~~~~~~~~~~~~~~

To deploy a site template:

::

    $ subfork deploy <template.yaml>
