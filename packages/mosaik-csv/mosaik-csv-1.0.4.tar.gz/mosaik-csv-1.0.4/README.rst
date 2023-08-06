mosaik-csv
==========

This is pseudo simulator that presents CSV data sets to mosaik as models.


Installation
------------

::

    $ pip install mosaik-csv

Tests
-----

You can run the tests with::

    $ git clone https://gitlab.com/mosaik/mosaik-csv.git
    $ cd mosaik-csv
    $ pip install -r requirements.txt
    $ pip install -e .
    $ py.test
    $ tox

If installation of psutil fails, installing python developer edition and gcc should help::

    $ sudo apt-get install gcc python3-dev
