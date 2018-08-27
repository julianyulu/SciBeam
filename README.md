
[![logo](https://raw.githubusercontent.com/SuperYuLu/SciBeam/master/img/logo.png)](https://github.com/SuperYuLu/SciBeam)  

# SciBeam [![Build Status](https://travis-ci.org/SuperYuLu/SciBeam.svg?branch=master)](https://travis-ci.org/SuperYuLu/SciBeam) [![codecov](https://codecov.io/gh/SuperYuLu/SciBeam/branch/master/graph/badge.svg)](https://codecov.io/gh/SuperYuLu/SciBeam) [![PyPI version](https://badge.fury.io/py/scibeam.svg)](https://badge.fury.io/py/scibeam) [![Documentation Status](https://readthedocs.org/projects/scibeam/badge/?version=latest)](https://scibeam.readthedocs.io/en/latest/?badge=latest)  



**scibeam** is a python package build on top of pandas, numpy, sicpy and matplotlib. It is aimed for quick and easy scientific time-series data analysis and visualization in physics, optics, mechanics, and many other STEM subjects.  

In the context of scientific data analysis, there are a lot of situations that people have to deal with time-series data, such as time dependent experiment(e.g. temperature measurement), dynamic processes(e.g. beam propagation, chemical reaction), system long/short term behavior(e.g. noise), etc. Quite often is that data taking and result analysis is gaped by some time and effort, which could result in complains or regrets during the data analysis, like “I wish I took another measurement of … so than I could explain why …”. As such, the general guidline of scibeam is to bridge the gap between measurement and data analysis, so that time-series related experiment can be done in a more guided way.  

The basic features of scibeam include but not limited to: beam propagation, single or multi-dimentional time depedent measurement, data file auto indexing, noise reduction, peak analysis, numerical fittings, etc.  

# Installation  

## Dependencies  
SciBeam requires:  

+ Python( >= 3.4)
+ Numpy( >= 1.8.2)
+ Scipy( >= 0.13.3)
+ pandas ( >= 0.23.0)
+ matplotlib ( >= 1.5.1)
+ re
+ os 

## User installation  
Currently only avaliable through downloading from Github, will be avaliable for installation through pip soon:  

### Using PyPI  

```bash
pip install scibeam  
```

### Using souce code   

Download the souce code:  

```bash
git clone https://github.com/SuperYuLu/SciBeam`  
```

Change to the package directory:  

```bash
cd scibeam  
```

Install the package:  

```
python setup.py install  
```

# Documents
All documentation is avaliable [here](https://scibeam.readthedocs.io/en/latest/?badge=latest)  


# Release  
+ v0.1.0: 08/19/2018  first release !
+ v0.1.1: 08/22/2018  first release !

# Development  
Under active development. 

## TODO:  
+ Increase test coverage 
+ Add more plotting functions
+ Add config.py for global configurature 
+ Add AppVeyor 

## Contribute  

**Call for contributors !**  


As a open source project, scibeam is under active development towards version 1.0, thus we need contributors from the conmunity.Please follow the steps if you want to contribute:  

+ Read the [documents](https://scibeam.readthedocs.io/en/latest/?badge=latest)
+ Join the [slack channel](https://scibeam.slack.com)
+ Report issure / bug on Github
+ Look for open [issues](https://github.com/SuperYuLu/SciBeam/issues)
+ Create new pull request


## Testing  
The testing part is based on unittest and can be run through setuptools, please refer to the [documents](https://scibeam.readthedocs.io/en/latest/?badge=latest)  

To run the test:  
```python
python setup.py test  
```

or 

```bash
make test
```


## Status  
Version 0.1.1 on [PyPI](https://pypi.org/project/scibeam/)
