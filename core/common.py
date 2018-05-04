# common.py --- 
# 
# Filename: common.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri May  4 11:32:04 2018 (-0500)
# Version: 
# Last-Updated: Fri May  4 12:09:45 2018 (-0500)
#           By: yulu
#     Update #: 11
# 
import os
import numpy as np


def winPathHandler(args):
    """
    convert windows path variables to python/linux compatible
    """

    def strPathHandler(stringPath):
        if isinstance(stringPath, str):
            result_path =  stringPath.replace('\\', '/')
        else:
            print("path must be string for format handelling")
            raise TypeError
        if os.path.isdir(result_path):
            result_path = result_path + '/' if not result_path[-1] == '/' else result_path
        return result_path
    
    if isinstance(args, str):
        return strPathHandler(args)

    elif hasattr(args, '__iter__'):
        result_path = []
        for element_arg in args:
            result_path.append(strPathHandler(element_arg))
        return result_path

def loadFile(filename, cols = 2, usecols = None, skiprows = 0, kind = 'txt', sep = '\t'):
    if os.path.isfile(filename):
        pass
    else:
        print("File %s not found!" %filename)
        raise FileNotFoundError

    if kind == 'txt' or kind == 'lvm':
        try:
            data = np.fromfile(filename, sep = sep).reshape(-1, cols)
        except ValueError:
            # not complete
            print("You haven't finised this error exception !")
            pass

        try:
            data = np.loadtxt(filename, delimiter = sep, skiprows = skiprows, usecols = usecols)
        except ValueError:
            print("You haven't finised this error exception !")
            pass
        
        return data

    if kind== 'csv':
        print("You haven't finised this block !")
        pass

    else:
        print("Function loadFile cannot handle this file:\n\t%s" %filename)
    
