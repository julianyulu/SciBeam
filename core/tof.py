# tof.py --- 
# 
# Filename: tof.py
# Description: 
#            single time-of-flight data series analysis
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri May  4 10:53:40 2018 (-0500)
# Version: 
# Last-Updated: Sun May  6 16:44:26 2018 (-0500)
#           By: yulu
#     Update #: 292
# 


import numpy as np
import pandas as pd
import os
import re

from SciBeam.core.common import Common
from SciBeam.core.regexp import RegExp    
from SciBeam.core.timeseries import TimeSeries
from SciBeam.core import base
from SciBeam.core.descriptor import DescriptorMixin

class TOF:
    
    """
    Single time-of-flight data analysis
    data: value of tof measure, shape(len(labels), len(times))
    time: time, 1D array of time for each tof data point
    label: label of the tof measurement, for mulitple same tof measurement 
           under different conditions, e.g. sensor position, etc. 
    time_unit: unit for time, optional, default None
    value_unit: unit for tof values, default None
    """
    
    def __init__(self, values, time = [], labels = None, time_unit = None, value_unit = None):
        self.data = values
        self.time = time
        self.labels = labels
        self.time_unit = time_unit
        self.value_unit = value_unit
        self.df = self.__to_DataFrame()
        
        

    def __repr__(self):
        return repr(self.df)
    
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, values):
        d = np.array(values)
        if d.ndim == 1:
            d = d.reshape(1, -1)
        self.__data = d
        

    @property
    def time(self):
        return self.__time
    
    @time.setter
    def time(self, time):
        datalen = self.__data.shape[1]
        if len(time) > 0  and len(time) == datalen: # set time to provided value
            unique_time_step = np.unique(np.diff(time))
            unique_time_step = [x for x in unique_time_step if abs(x - unique_time_step.mean()) > unique_time_step.mean()/ 100] 
            if len(unique_time_step) > 1:
                print("[*] Warning: Non-unique time step size detected in time")
                print("[!] Time step sizes: ", unique_time_step)
            else:
                pass
            self.__time = np.array(time)
            try: # try update time in df if exists
                self.df.index = time
            except (ValueError, AttributeError):
                pass
        else:
            self.__time = np.arange(self.data.shape[1]) # set to defaults
            
    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        if labels and len(self.__data) == len(labels):
            self.__labels = labels
            try: # try update labels in df in exists
                self.df.columns = labels
            except AttributeError:
                pass
        else:
            self.__labels = labels
    
                
        
    def __to_DataFrame(self):
        """
        Convert data to pandas DataFrame
        Index: time
        Columns: different values measured under same time 
        """
        
        # set value
        df = pd.DataFrame(self.__data.T)
        # set labels
        if self.__labels:
            df.columns =  self.__labels
        else:
            if self.__data.shape[0] > 1:
                df.columns = ['tof_' + str(i) for i in range(self.__data.shape[0])]
            else:
                df.columns = ['tof']
        # set time
        try:
            df.index  = self.__time
            
        except ValueError:
            pass
                
        return df

    
        
    @classmethod
    def fromfile(cls, path, regStr = None, lowerBound = None, upperBound = None,
                 removeOffset = True, cols = 2, usecols = None, skiprows = 0,
                 kind = 'txt', sep = '\t'):

        """
        Buid TOF instance from given file
        Current only works for '\t' seperated txt and lvm file
        """
        
        path = Common.winPathHandler(path)
        # If given folder path
        if os.path.isdir(path):
            if regStr:
                keys, files = RegExp.fileMatch(path, regStr)
                data = []
                for f in files:
                    d = Common.loadFile(path + f, cols = cols, usecols = usecols,skiprows = skiprows, kind = kind, sep = sep)
                    if lowerBound and upperBound:
                        d = _select_time_bound_data(d, lowerBound, upperBound, removeOffset = removeOffset)
                    else:
                        pass
                    data.append(d[:,1])
                time = d[:,0]
                return cls(data, time = time, labels = keys)
            else:
                print("[*] Please provide regStr for file match in the path !")

        # if given file path
        else:
            d = Common.loadFile(path, cols = cols, usecols = usecols,skiprows = skiprows, kind = kind, sep = sep)
            if lowerBound and upperBound:
                d = _select_time_bound_data(d, lowerBound, upperBound, removeOffset = removeOffset)
            else:
                pass
            time = d[:,0]
            data = d[:,1]
            return cls(data, time = time)
                

    @property
    def shape(self):
        return self.__data.shape

    @property
    def info(self):
        """
        General info string of the class obj.
        """
        delta_t = np.unique(self.df.index)
        max_value = max(self.df.max())
        min_value = min(self.df.min())
        start_t = min(self.df.index)
        end_t = max(self.df.index)

        info_str = '\n'.join([
            'SciBeam.TOF.info:',
            '--------------------',
            'data value shape: %s'    %str(self.__data.shape),
            'total data points: %d'   %self.__data.size,
            'Start time: %f'          %start_t,
            'End time: %f'            %end_t,
            'Max value: %f'           %max_value,
            'Min value: %f'           %min_value,
            '--------------------'])
        print(info_str)
    


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
                    
        
                
    def selectTimeSlice(self, *args):
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
        for arg_elem in self.find_time_idx(self.time, args):
            if hasattr(arg_elem, '__iter__'):
                for t in arg_elem:
                    slice_value.append(self.df.iloc[t])
            else:
                slice_value.append(self.df.iloc[arg_elem])
        slice_DataFrame = pd.DataFrame(slice_value)
        return slice_DataFrame

    def selectTimeRange(self, lowerBound, upperBound):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = self.find_time_idx(self.time, lowerBound, upperBound)
        return self.df.iloc[lb:ub, :].copy() # Dataframe
    

    
    @property
    def describe(self):
        return self.df.describe()
        
    @property
    def _make_mixin(self):
        return self.df




    
    #single = DescriptorMixin(TimeSeries)
    
# Class Tof end <---




###
# Functions
###
def _find_time_bound_idx(time, lowerBound, upperBound):
    """
    find the index of time lower and upper bounds in the given time data
    """
    time = np.array(time)
    t_max_gap = np.max(np.diff(time))
    idx = []
    for t in [lowerBound, upperBound]:
        candi_idx = np.argmin(abs(t - time))
        if abs(t - time[candi_idx]) > t_max_gap:
            raise ValueError("\n[*] Error: find_time_idx didn't find closest match !\n" + 
                             "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                             %(t, time[candi_idx]))
        else: 
            idx.append(candi_idx)

    return idx[0], idx[1]

    
def _select_time_bound_data(data, lowerBound, upperBound, removeOffset = True,
                             offset_detect_margin = 20):
    lb, ub = _find_time_bound_idx(data[:,0], lowerBound, upperBound)
    if removeOffset:
        while True:
            try:
                offset = (np.average(data[lb-offset_detect_margin:lb, 1]) +
                          np.average(data[ub:ub + offset_detect_margin, 1])) / 2
                break
            except IndexError:
                offset_detect_margin = offset_detect_margin - 1
            else:
                pass
        data[:,1] = data[:,1] - offset
            
    else:
        pass
    data = data[lb:ub, :]
    return data
    
