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
# Last-Updated: Thu Jul 19 11:43:26 2018 (-0500)
#           By: yulu
#     Update #: 70
# 
import os

_mixin_class = ["<class 'SciBeam.core.tofseries.TOFSeries'>",
                "<class 'SciBeam.core.tofframe.TOFFrame'>",
                ]


def _is_mixin(att):
    for cls in _mixin_class:
        if str(type(att)) == cls:
            return True
    
    return False
    

class Defaults:

    # Top level
    #-----------------
    data_file_extenstion = '.lvm'
    data_file_num_column = 2
    # Lower level
    # ----------------
    subfolder_regex = '.*(\d+\.?\d+).*'
    file_regex = '.*_(\d+\.?\d+).*' + data_file_extenstion + '$'

    # Unit tests

            
