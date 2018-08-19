# base.py --- 
# 
# Filename: base.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun Mar 25 22:03:54 2018 (-0500)
# Version: 
# Last-Updated: Sun Aug 19 15:29:14 2018 (-0500)
#           By: yulu
#     Update #: 80
#

"""
Base functions for mixin classes and module width constants

Attributes
----------
_mixin_class: list(str)
  Specify allowed mixin class for method chain.
  The two basic data structures are TOFSeries and TOFFrame,                
  current.

Note
----
TODO: Move Defaults to a seperate config.py file for easy
configuration

"""
import os

_mixin_class = ["<class 'scibeam.core.tofseries.TOFSeries'>",
                "<class 'scibeam.core.tofframe.TOFFrame'>",
                ]


def _is_mixin(att):
    """check if attribute is of allowed mixin class
    
    The attribute has to be one of the allowed mixin classes specified
    in '_mixin_class' to be considered as mixin attribute.

    """
    for cls in _mixin_class:
        if str(type(att)) == cls:
            return True
    
    return False
    

class Defaults:
    """Module level default values 
    
    Settings for global default values
    
    Note
    ----
    TODO: realize these using a seperate config.py file

    """
    
    # Top level
    #-----------------
    data_file_extenstion = '.lvm'
    data_file_num_column = 2
    # Lower level
    # ----------------
    subfolder_regex = '.*(\d+\.?\d+).*'
    file_regex = '.*_(\d+\.?\d+).*' + data_file_extenstion + '$'
    # Unit tests

            
