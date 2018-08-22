# setup.py --- 
# 
# Filename: setup.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat Jul 21 10:46:04 2018 (-0500)
# Version: 
# Last-Updated: Wed Aug 22 11:36:12 2018 (-0500)
#           By: yulu
#     Update #: 82
# 

from setuptools import setup

with open("README.rst") as f:
    README = f.read()

setup(
    name = 'scibeam',
    version = '0.1.1',
    author = 'Yu Lu',
    author_email = 'yulu@utexas.edu',
    url = 'https://github.com/SuperYuLu/SciBeam',
    packages = ['scibeam', 'scibeam.tests', 'scibeam.core', 'scibeam.util'],
    license = 'LICENSE.txt',
    description = 'Library for scientific time series dat aanalysis and visualization on beam measurement',
    long_description = README,
    #long_description_content_type='text/markdown',
    install_requires = ['numpy',
                        'pandas',
                        'scipy',
                        'matplotlib'],
    
    #test_suite = 'nose.collector',
    #test_suite = 'tests',
    #tests_require = ['nose'],

    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        ],
    
    keywords = 'physics time-series data-analysis pandas',
    
    package_data = {'scibeam': ['data/examples/time_series_1D/single_time_series.lvm',
                                'data/examples/time_series_2D/*.lvm',
                                'data/test/time_series_1D/single_time_series.lvm',
                                'data/test/time_series_2D/*.lvm'
    ]},
)
