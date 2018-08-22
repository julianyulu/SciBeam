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
# Last-Updated: Sun Aug 19 15:31:59 2018 (-0500)
#           By: yulu
#     Update #: 36
#

"""
Common functions used across classes and modules
"""


import os
import numpy as np

__all__ = [
    'winPathHandler',
    'loadFile',
    ]

def winPathHandler(args):
    """A windows path string handler

    Convert windows path string variables to python/linux compatible Path

    Parameters
    ----------
    args : string
        A single or list of strings of path

    Returns
    -------
    string
        Reformated string of list of strings

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
        else:
            return result_path

    if isinstance(args, str):
        return strPathHandler(args)

    elif type(args) == list:
        result_path = []
        for element_arg in args:
            result_path.append(strPathHandler(element_arg))
        return result_path
    else:
        print("[*] Path not understood !")
        print("[!] Please make sure it's in Windows/Linux format")
        return 0


def loadFile(filename, cols = 2, usecols = None, skiprows = 0, kind = 'txt', sep = '\t'):
    """File loader

    Loading txt / lvm data files

    Parameters
    ----------
    filename : string
        Filename string (including the full path to the file)
    cols : int
        Total number of columns to be loaded, default 2
    usecols : int
        Column to be used, if None then load all. Default None
    skiprows : int
        Number of rows to skip when loading data, this is specifically designed
        for the case that there is header in the file
    kind : string
        File format, default 'txt'.
        Currently only works for txt-like files
    sep : string
        Seperator of the data column, default '\t'

    Returns
    -------
    numpy.ndarray
        data loaded as numpy ndarray, default 2D array

    Raises
    ------
    FileNotFoundError
        File not found with given filename string
    ValueError
        Data loading didn't finish
        
    """
    if os.path.isfile(filename):
        pass
    else:
        print("File %s not found!" %filename)
        raise FileNotFoundError

    if kind == 'txt' or kind == 'lvm':
        try:
            data = np.fromfile(filename, sep = sep).reshape(-1, cols)
            data = data[skiprows:,usecols] if usecols else data
        except ValueError:
            # not complete
            print("You haven't finised this error exception !")
            pass
            ##
            # Slow algorithm
            ##

            # try:
            #     data = np.loadtxt(filename, delimiter = sep, skiprows = skiprows, usecols = usecols)
            # except ValueError:
            #     print("You haven't finised this error exception !")
            #     pass

        return data

    if kind== 'csv':
        print("You haven't finised this block !")
        pass

    else:
        print("Function loadFile cannot handle this file:\n\t%s" %filename)
