|logo|

SciBeam |Build Status| |codecov| |PyPI version|
===============================================

**SciBeam** is an open source library for analyzing time series beam
measurement data. Using pandas dataframe and series as its base
classing, additional time series related features are added for quick
analysis, such as file name matching, gaussian fitting, peak analysis,
noise filtering, plotting, etc. The flexible method chain enables fast
data analysis on any time series data.

SciBeam is originally designed for experimental physics data analysis.
The library has been tested on the daily lab data analysis and is under
active development in terms of bredth and deepth of scientific
computation.

Installation
============

Dependencies
------------

SciBeam requires:

-  Python( >= 3.4)
-  Numpy( >= 1.8.2)
-  Scipy( >= 0.13.3)
-  pandas ( >= 0.23.0)
-  matplotlib ( >= 1.5.1)
-  re
-  os

User installation
-----------------

Currently only avaliable through downloading from Github, will be
avaliable for installation through pip soon:

Using PyPI
~~~~~~~~~~

.. code:: bash

   pip install scibeam  

Using souce code
~~~~~~~~~~~~~~~~

Download the souce code:

.. code:: bash

   git clone https://github.com/SuperYuLu/SciBeam`  

Change to the package directory:

.. code:: bash

   cd scibeam  

Install the package:

::

   python setup.py install  

Release
=======

-  v0.1.0: 08/19/2018 first release !

Development
===========

Under active development.

TODO:
-----

-  Increase test coverage
-  Add more plotting functions
-  Add config.py for global configurature
-  Add AppVeyor

Contribute
----------

Coming soon…

Testing
-------

The testing part is based on unittest and can be run through setuptools:

.. code:: python

   python setup.py test  

or

.. code:: bash

   make test

Status
------

Version 0.1.0 on `PyPI <https://pypi.org/project/scibeam/>`__

.. |logo| image:: https://raw.githubusercontent.com/SuperYuLu/SciBeam/master/img/logo.png
   :target: https://github.com/SuperYuLu/SciBeam
.. |Build Status| image:: https://travis-ci.org/SuperYuLu/SciBeam.svg?branch=master
   :target: https://travis-ci.org/SuperYuLu/SciBeam
.. |codecov| image:: https://codecov.io/gh/SuperYuLu/SciBeam/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/SuperYuLu/SciBeam
.. |PyPI version| image:: https://badge.fury.io/py/scibeam.svg
   :target: https://badge.fury.io/py/scibeam
