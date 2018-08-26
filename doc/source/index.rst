.. scibeam documentation master file, created by
   sphinx-quickstart on Sun Aug 19 13:16:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SciBeam
===================================
.. image:: ../../../img/logo.png
    :width: 700px
    :alt: scibeam logo
    :align: center

.. image:: https://travis-ci.org/SuperYuLu/SciBeam.svg?branch=master
   :target: https://travis-ci.org/SuperYuLu/SciBeam
   :alt: Build Status

.. image:: https://codecov.io/gh/SuperYuLu/SciBeam/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/SuperYuLu/SciBeam
   :alt: codecov

.. image:: https://readthedocs.org/projects/scibeam/badge/?version=latest
   :target: https://scibeam.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
	 
.. image:: https://badge.fury.io/py/scibeam.svg
   :target: https://badge.fury.io/py/scibeam
   :alt: PyPI version
      


SciBeam is a python package build on top of pandas, numpy, sicpy and matplotlib. It is  aimed for quick and easy scientific time-series data analysis and visualization in physics, optics, mechanics, and many other STEM subjects. 

In the context of scientific data analysis, there are a lot of situations that people have to deal with time-series data, such as time dependent experiment(e.g. temperature measurement), dynamic processes(e.g. beam propagation, chemical reaction), system long/short term behavior(e.g. noise), etc. Quite often is that data taking and result analysis is gaped by some time and effort, which could result in complains or regrets during the data analysis,  like "I wish I took another measurement of ... so than I could explain why ...". As such, the general guidline of scibeam is to bridge the gap between measurement and data analysis, so that time-series related experiment can be done in a more guided way. 

The basic features of scibeam include but not limited to: beam propagation, single or multi-dimentional time depedent measurement, data file auto indexing, noise reduction, peak analysis, numerical fittings, etc.
	   
	   
.. toctree::
   :maxdepth: 2
   :caption: GENERAL

   about
.. toctree::
   :maxdepth: 2
   :caption: GETTING STARTED

   install
   structure

.. toctree::
   :maxdepth: 2
   :caption: THE SCIBEAM PACKAGE
	     
   scibeam

.. toctree::
   :maxdepth: 2
   :caption: DEVELOP
	     
   scibeam.tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
