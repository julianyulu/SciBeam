Install
=======
Install scibeam is easy, one can choose either install using pypi or from `source code`_ using python setuptools.

Requirements
------------
The scibeam package requires:

+ Python(>= 3.4)
+ Numpy
+ Scipy
+ Pandas
+ matplotlib

.. note::
   
   scibeam doesn't support python 2.7, make sure you have the right python version (>=3.4).

Using PyPI
----------
Scibeam is avaliable on PyPI_, one can install under python3 environment using::

  pip install scibeam

Scibeam can then be imported as::

  import scibeam

  

Using Setuptools
----------------
To install using python setuptools, simply clone the source code::

  git clone git@github.com:SuperYuLu/SciBeam.git

Then change into the SciBeam folder::

  cd SciBeam

Under SciBeam folder, install by typing::

  python setup.py install

scibeam package name should be then available in the python environment, to import::

  import scibeam

or::
  
  from scibeam import *


.. _source code: https://github.com/SuperYuLu/SciBeam
.. _PyPI: https://pypi.org/project/scibeam/
