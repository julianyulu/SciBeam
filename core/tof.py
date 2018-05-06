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
# Last-Updated: Sun May  6 00:06:45 2018 (-0500)
#           By: yulu
#     Update #: 162
# 


import numpy as np
import pandas as pd
import os
import re

from SciBeam.core.common import Common
from SciBeam.core.regexp import RegExp    
from SciBeam.core.timeseriesanalysis import TimeSeries
from SciBeam.core import base
from SciBeam.core.descriptor import DescriptorMixin

class TOF:
    
    """
    Single time-of-flight data analysis
    """
    
    def __init__(self, values, time = [], labels = None, time_unit = None, value_unit = None):
        self.data = values
        self.time = time
        self.labels = labels
        self.time_unit = time_unit
        self.value_unit = value_unit
        self.df = self.__to_DataFrame()
        
        

    def __repr__(self):
        return self.__info()
    
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, values):
        self.__data = np.array(values)

    @property
    def time(self):
        return self.__time
    
    @time.setter
    def time(self, time):
        datalen = len(self.__data) if len(self.__data.shape) == 1  else self.__data.size / self.__data.shape[0]
        if len(time) > 0  and len(time) == datalen: # set time to provided value
            self.__time = time
            try: # try update time in df if exists
                self.df.time = time
            except (ValueError, AttributeError):
                pass
        else: # set time to default value 
            try:
                self.__time = np.arange(self.data.shape[1]) # 2d data array
            except IndexError:
                self.__time = np.arange(len(self.data)) # 1d data array

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        if labels and len(self.data) == len(labels):
            self.__labels = labels
            try: # try update labels in df in exists
                self.df.columns = ['time'] + labels
            except AttributeError:
                pass
        else:
            self.__labels = labels
    
                
        
    def __to_DataFrame(self):
        """
        Conver data to pandas DataFrame
        """
        
        # set value
        df = pd.DataFrame(self.__data.T)
        # set labels
        if self.__labels:
            df.columns =  self.__labels
        else:
            if len(self.__data.shape) > 1:
                df.columns = ['tof_' + str(i) for i in range(self.__data.shape[0])]
            else:
                df.columns = ['tof']
        # set time
        try:
            df['time']  = self.__time
        except ValueError:
            pass
        # time as the first column
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        
        return df

    @staticmethod
    def __find_time_bound_idx(time, lowerBound, upperBound):
        """
        find the index of time lower and upper bounds in the given time data
        """
        time = np.array(time)
        lb = np.argmin(abs(time - lowerBound))
        ub = np.argmax(abs(time - upperBound))
        return lb, ub

    @staticmethod
    def __select_time_bound_data(data, lowerBound, upperBound, removeOffset = True,
                                 offset_detect_margin = 20):
        lb, ub = self.__find_time_bound_idx(time, lowerBound, upperBound)
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
            d[:,1] = d[:,1] - offset
            
        else:
            pass
        data = data[lb:ub, :]
        return data
        
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
                        d = self.__select_time_bound_data(d, lowerBound, upperBound, removeOffset = removeOffset)
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
                d = self.__select_time_bound_data(d, lowerBound, upperBound, removeOffset = removeOffset)
            else:
                pass
            time = d[:,0]
            data = d[:,1]
            return cls(data, time = time)
                

    @property
    def shape(self):
        return self.__data.shape

    
    def __info(self):
        """
        General info string of the class obj.
        """
        delta_t = np.unique(self.df.time)
        max_value = max(self.df.max())
        min_value = min(self.df.min())
        start_t = min(self.time)
        end_t = max(self.time)

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
        return info_str

    @property
    def _make_mixin(self):
        return self.df

    ts = DescriptorMixin(TimeSeries)
    
                            
