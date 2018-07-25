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
# Last-Updated: Tue Jul 24 23:48:30 2018 (-0500)
#           By: yulu
#     Update #: 27
# 

from setuptools import setup

setup(
    name = 'SciBeam',
    version = '0.1.0',
    author = 'Yu Lu',
    author_email = 'yulu@utexas.edu',
    url = 'https://github.com/SuperYuLu/SciBeam',
    packages = ['scibeam', 'scibeam.tests'],
    license = 'LICENSE.txt',
    description = 'A Scientific time series analyzing tool on beam measurement',
    long_description = open('README.txt').read(), 
    install_requires = ['numpy',
                        'pandas',
                        'scipy',
                        'matplotlib'],
                        
    test_suite = 'nose.collector',
    #test_suite = 'tests',
    tests_require = ['nose'],
    classifiers = [
        'Development status :: 3 - Alpha',
        'Intended Audience :: Researchers',
        'Topic :: Physics :: Data Analyzing Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        ],
    keywords = 'physics beam data analyzing',
        package_data = {
        'example': ['examples/data/time_series_1D/single_time_series.lvm']
        }
    
    
    
    
    )
