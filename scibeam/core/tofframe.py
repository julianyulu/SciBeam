# tofframe.py --- 
# 
# Filename: tofframe.py
# Description: 
#            DataFrame for  time-of-flight data frame analysis
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri May  4 10:53:40 2018 (-0500)
# Version: 
# Last-Updated: Sat Jul 21 07:31:24 2018 (-0500)
#           By: yulu
#     Update #: 744
# 




import os
import re
import pandas
import numpy as np
import matplotlib.pyplot as plt

from SciBeam.core import base
from SciBeam.core import tofseries
from SciBeam.core.common import winPathHandler, loadFile
from SciBeam.core.regexp import RegMatch
from SciBeam.core.descriptor import DescriptorMixin
from SciBeam.core.plot import PlotTOFFrame
from SciBeam.core.peak import FramePeak


def read_folder(path, regStr,
                lowerBound = None,
                upperBound = None,
                removeOffset = True,
                offset_margin_how = 'outer',
                offset_margin_size = 20, skiprows = 0, sep = '\t'):
    """
    Create TOFFrame class instance by reading in group of files in a folder matched by regex 
    
    Parameters
    -----------

    path: str 
          folder path, linux style or windows style as "raw string", e.g. r"C:\\User\\Document\\FolderName"
    lowerBound: int or float
                time axis lower boundrary limit for data
    upperBound: int or float 
                time axis upper boundrary limit for data
    removeOffset: bool 
                  if True (default) remove data offset (set floor to 0 in no-signal region) 

    offset_margin_how: {"outer", "outer left", "out right", "inner", "inner left", "inner right"}, default "outer"

                       Specify the way to handle offset margin, offset floor value is calculated by averaging the 
                       value in a given range relative to data lower and upper boundrary, with avaliable options:

                       * "outer" (default):  from both left and right side out of the [lowerBound, upperBound] region
                       * "outer left": like "outer" but from only left side 
                       * "outer right": like "outer" but from only right side 
                       * "inner": from both left and right side inside of the [lowerBound, upperBound] region
                       * "inner left": like "inner" but from only left side 
                       * "inner right": like "inner" but from only left side 

    offset_margin_size: int 
                        Number of values to use for averaging when calculating offset 
    skiprows: int 
              number of rows to skip when read in data 
    sep: str, defult "\t"
         seperator for columns in the data file

    Returns:
    --------
    Instance of class TOFFrame 
    """
    return TOFFrame.from_path(path, regStr,
                              lowerBound = lowerBound, upperBound = upperBound,
                              removeOffset =removeOffset,
                              offset_margin_how = offset_margin_how,
                              offset_margin_size = offset_margin_size,
                              skiprows = sikprows,  sep = sep)



def read_regexp_match(path, matchDict,
                      lowerBound = None,
                      upperBound = None,
                      removeOffset = True,
                      offset_margin_how = 'outer',
                      offset_margin_size = 20, skiprows = 0, sep = '\t'):
    """
    Create instance of TOFFrame from regular expression match result dictionary
    using SciBeam class RegMatch 
    
    Parameters
    ----------
    path: str
          path of the targeted data folder 
    matchDict: dictionary 
               result dictionary form SciBeam.regexp.RegMatch, or user specified 
               dictionary with key as measurement label, value as file name string
    lowerBound: int or float
                time axis lower boundrary limit for data
    upperBound: int or float 
                time axis upper boundrary limit for data
    removeOffset: bool 
                  if True (default) remove data offset (set floor to 0 in no-signal region) 

    offset_margin_how: {"outer", "outer left", "out right", "inner", "inner left", "inner right"}, default "outer"

                       Specify the way to handle offset margin, offset floor value is calculated by averaging the 
                       value in a given range relative to data lower and upper boundrary, with avaliable options:

                       * "outer" (default):  from both left and right side out of the [lowerBound, upperBound] region
                       * "outer left": like "outer" but from only left side 
                       * "outer right": like "outer" but from only right side 
                       * "inner": from both left and right side inside of the [lowerBound, upperBound] region
                       * "inner left": like "inner" but from only left side 
                       * "inner right": like "inner" but from only left side 

    offset_margin_size: int 
                        Number of values to use for averaging when calculating offset 
    skiprows: int 
              number of rows to skip when read in data 
    sep: str, defult "\t"
         seperator for columns in the data file

    Returns
    -------
    Instance of TOFFrame
    """
    
    return TOFFrame.from_matchResult(path, matchDict,
                                     lowerBound = lowerBound, upperBound = upperBound,
                                     removeOffset = removeOffset,
                                     offset_margin_how = offset_margin_how,
                                     offset_margin_size = offset_margin_size,
                                     skiprows = skiprows, sep = sep)



class TOFFrame(pandas.DataFrame):
    
    """
    Time-Of-Flight (TOF) DataFrame 
    
    Subclassing pandas.DataFrame with extral methods / properties for time-series analysis 

    Parameters
    -----------
    data: numpy ndarray (structured or homogeneous), dict, or DataFrame                          
          Dict can contain Series, arrays, constants, or list-like objectsSingle time-of-flight data analysis
          Value of measurement, e.g. voltage, current, arbiturary unit signel, shape(len(labels), len(times))
    index: numpy ndarray, iterables 
          Time axis for time-of-flight 
    columns: str, int, or float 
             label of different tof measurement, e.g. pressure, temperature, etc
    """
    pandas.set_option('precision', 9)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _constructor(self):
        return TOFFrame
    @property
    def _constructor_sliced(self):
        return tofseries.TOFSeries
    
    @property
    def _make_mixin(self):
        return self.copy()
            
    def _toTOFSeries(func):
        """
        Decorator to wrap series returns for method chain 
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) == pandas.core.series.Series:
                return tofseries.TOFSeries(result)
            else:
                return result
        return wrapper

    
    def _toTOFFrame(func):
        """
        Decorator to wrap frame returns for method chain 
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) == pandas.core.frame.DataFrame:
                return TOFFrame(result)
            else:
                return result
        return wrapper


    @classmethod
    def from_path(cls, path, regStr, lowerBound = None, upperBound = None, removeOffset = True,
                offset_margin_how = 'outer', offset_margin_size = 20, skiprows = 0, sep = '\t'):
        """
        Buid TOFFrome instance from given file folder
        Current only works for '\t' seperated txt and lvm file
        """

        path = winPathHandler(path)
        
        matchDict = RegMatch(regStr).matchFolder(path)
        if type(regStr) == str:
            keys, files = zip(*sorted(matchDict.items(), key = lambda x: x[0]))
            values = {}
            for k, f in zip(keys, files):
                try:
                    data = loadFile(path + f, skiprows = skiprows, sep = sep)
                except TypeError:
                    print("[*] Multiple files found under the same parameter, please check below files:\n", f)
                    raise TypeError
                if lowerBound and upperBound:
                    lb, ub = TOFFrame.find_time_idx(data[:, 0], lowerBound, upperBound)
                    time = data[lb:ub, 0]
                    if removeOffset:
                        value = TOFFrame.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, how = offset_margin_how, margin_size = offset_margin_size)
                    else:
                        value = data[lb:ub, 1]
                else:
                    time = data[:, 0]
                    value = data[:, 1]
                values[k] =  value    
        else:
            raise ValueError("[*] Please provide regStr for file match in the path !")
        return cls(values, index = time)
    
    @classmethod
    def from_file(cls, filePath,  lowerBound = None, upperBound = None, removeOffset = True,
                offset_margin_how = 'outer', offset_margin_size = 20, skiprows = 0, sep = '\t'):
        """
        Generate TOFFrame object from a single given file
        """
        
        filePath = winPathHandler(filePath)
        data = loadFile(filePath, skiprows = skiprows,  sep = sep)
        if lowerBound and upperBound:
            lb, ub = TOFFrame.find_time_idx(data[:,0], lowerbound, upperBound)
            time = data[lb : ub, 0]
            if removeOffset:
                value = TOFFrame.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, how = offset_margin_how, margin_size = offset_margin_size)
            else:
                value = data[lb:ub, 1]
        else:
            time = data[:,0]
            value = data[:,1]
        values = {'value':value}
        return cls(values, index = time)

    
    @classmethod
    def from_matchResult(cls, path, matchDict, lowerBound = None, upperBound = None, removeOffset = True,
                offset_margin_how = 'outer', offset_margin_size = 20, skiprows = 0, sep = '\t'):
        """
        Creat TOFFrame from a RegMatch resutl dictionary
        """

        path = winPathHandler(path)
        # If given folder path
        if os.path.isdir(path):
            
            keys, files = zip(*sorted(matchDict.items(), key = lambda x: x[0]))
            values = {}
            for k, f in zip(keys, files):
                data = loadFile(path + f, skiprows = skiprows, sep = sep)
                if lowerBound and upperBound:
                    lb, ub = TOFFrame.find_time_idx(data[:, 0], lowerBound, upperBound)
                    time = data[lb:ub, 0]
                    if removeOffset:
                        value = TOFFrame.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, how = offset_margin_how, margin_size = offset_margin_size)
                    else:
                        value = data[lb:ub, 1]
                else:
                    time = data[:, 0]
                    value = data[:, 1]
                values[k] =  value
            return cls(values, index = time)
        else:
            raise IsADirectoryError("[*] path not found!")
        

    
    @staticmethod
    def find_time_idx(time, *args):
        """
        Generator of time index for a given time value
        args: can be 1,2,3, or [1,2] or [1,2,3]
        """
        time = np.array(time)
        t_max_gap = np.max(np.diff(time))
        for arg_elem in args:
            
            if hasattr(arg_elem, '__iter__'):
                idx = []
                for t in arg_elem:
                    candi_idx = np.argmin(abs(t - time))
                    if abs(t - time[candi_idx]) > t_max_gap:
                        raise ValueError("[*] Error: find_time_idx didn't find closest match !\n" + 
                                         "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                                         %(t, time[candi_idx]))
                    else: 
                        idx.append(candi_idx)
                    yield idx
                    
            else:
                candi_idx = np.argmin(abs(arg_elem - time))
                if abs(arg_elem - time[candi_idx]) > t_max_gap:
                        raise ValueError("[*] Error: find_time_idx didn't find closest match !\n" + 
                                         "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                                         %(arg_elem, time[candi_idx]))
                else:
                    idx = candi_idx
                yield idx
                    
    @staticmethod
    def remove_data_offset(data, lowerBoundIdx = None, upperBoundIdx = None, how = 'outer', margin_size = 10):
        """
        remove offset in 1D array data
        """
        # check bound index assignment
        if lowerBoundIdx is None and upperBoundIdx is None:
            lowerBoundIdx = 0
            upperBoundIdx = len(data)
            if 'outer' in how:
                how = 'inner'
                print("[*] No bound index specified, using default full range !")
                print("[*] Outer margin offset forced to be *inner* !")
            else:
                pass
        elif lowerBoundIdx is None:
            lowerBoundIdx = 0
            if how in ['outer', 'outer left']:
                how = how.replace('outer', 'inner')
                print("[*] No lower bound index specified, using default 0 !")
                print("[*] Outer margin offset forced to be *inner* !")
            else:
                pass
        elif upperBoundIdx is None:
            upperBoundIdx = len(data)
            if how in ['outer', 'outer right']:
                how = how.replace('outer', 'inner')
                print("[*] No lower bound index specified, using default max length !")
                print("[*] Outer margin offset forced to be *inner* !")
            else:
                pass
        else:
            pass
        
        if how == 'outer':
            offset = (np.mean(data[lowerBoundIdx-margin_size: lowerBoundIdx]) + np.mean(data[upperBoundIdx : upperBoundIdx + margin_size]))  / 2.
        elif how == 'outer left':
            offset = np.mean(data[lowerBoundIdx-margin_size: lowerBoundIdx])
        elif how == 'outer right':
            offset = np.mean(data[upperBoundIdx : upperBoundIdx + margin_size])
        elif how == 'inner':
            offset = (np.mean(data[lowerBoundIdx: lowerBoundIdx + margin_size]) + np.mean(data[upperBoundIdx - margin_size: upperBoundIdx]))  / 2
        elif how == 'inner left':
            offset = np.mean(data[lowerBoundIdx: lowerBoundIdx + margin_size])
        elif how == 'inner right':
            offset = np.mean(data[upperBoundIdx - margin_size: upperBoundIdx])
        else:
            raise ValueError(("[*] how: %s not understood !\n" +
                              "[!] possible values of how: 'outer', 'outer left', 'outer right', 'inner', 'inner left', 'inner right'") % how)
        
        data = data[lowerBoundIdx:upperBoundIdx] - offset
        
        return data
    
    @_toTOFFrame
    def selectTimeSlice(self, *args, inplace = False):
        """
        makeSlice
        -------------
        Create descrete time sliced series, if want continus range, use makeTimeRange()
        [Input]
        :args: descrete time slicing values, can use timeSlice(1,2,3,4) or timeSlice([1,2,3,4])
        [Output]
        Series of sliced data
        """
        
        slice_value = []
        for arg_elem in self.find_time_idx(self.index, args):
            if hasattr(arg_elem, '__iter__'):
                for t in arg_elem:
                    slice_value.append(self.iloc[t])
            else:
                slice_value.append(self.iloc[arg_elem])
        slice_DataFrame = pandas.DataFrame(slice_value)
        if inplace:
            self.__init__(slice_DataFrame)
        else:
            return slice_DataFrame

    @_toTOFFrame
    def selectTimeRange(self, lowerBound, upperBound, inplace = False):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = TOFFrame.find_time_idx(self.index, lowerBound, upperBound)
        selected = self.iloc[lb:ub, :].copy()
        if inplace:
            self.__init__(selected)
        else:
            return selected

        
    @_toTOFSeries
    def sum(self, axis = 1):
        index = self.columns if axis == 0 else self.index
        sum_result = np.sum(self.values, axis = axis)
        return tofseries.TOFSeries(sum_result, index = index)

    
    @_toTOFFrame
    def inch_to_mm(self, offset_inch = 0, inplace = False):
        """
        convert inches to milimeters in the columns names
        """
        values = (self.columns -  offset_inch) * 25.4
        if inplace:
            self.columns = values
            return self
        else:
            return values
        
    @_toTOFFrame
    def mm_to_inch(self, offset_mm = 0, inplace = False):
        """
        convert milimeters to inches in the columns names
        """
        values = (self.columns -  offset_mm) /  25.4
        if inplace:
            self.columns = values
            return self
        else:
            return values
    
    @_toTOFFrame
    def sec_to_microsec(self, offset_sec = 0, inplace = False):
        """
        convert seconds in index to microseconds
        """
        times = (self.index - offset_sec) * 1e6
        if inplace:
            self.index = times
            return self
        else:
            return times
       
    @_toTOFFrame
    def microsec_to_sec(self, offset_microsec = 0, inplace = False):
        """
        convert microseconds in index to seconds
        """
        times = (self.index - offset_microsec) * 1e-6
        if inplace:
            self.index = times
            return self
        else:
            return times
    
    @_toTOFSeries
    def reduce(self, axis = 0):
        """
        reduce dimention from 2D to 1D by sum along axis
        """
        return self.sum(axis = axis)
    
    
    #Descriptors:
    #single = DescriptorMixin(TimeSeries)
    plot2d = DescriptorMixin(PlotTOFFrame)
    peak = DescriptorMixin(FramePeak)
