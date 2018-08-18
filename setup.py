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
# Last-Updated: Sat Aug 18 15:07:18 2018 (-0500)
#           By: yulu
#     Update #: 39
# 

from setuptools import setup


setup(
    name = 'scibeam',
    version = '0.1.1',
    author = 'Yu Lu',
    author_email = 'yulu@utexas.edu',
    url = 'https://github.com/SuperYuLu/SciBeam',
    packages = ['scibeam', 'scibeam.tests'],
    license = 'LICENSE.txt',
    description = 'A scientific time series analyzing tool on beam measurement',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires = ['numpy',
                        'pandas',
                        'scipy',
                        'matplotlib'],
    
                        
    test_suite = 'nose.collector',
    #test_suite = 'tests',
    tests_require = ['nose'],
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        ],
    keywords = 'physics time series data analyzing tool',
        package_data = {
        'example': ['examples/data/time_series_1D/single_time_series.lvm']
        }
    )
