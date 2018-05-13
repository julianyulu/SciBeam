# tofframe.py --- 
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
# Last-Updated: Sun May 13 12:54:10 2018 (-0500)
#           By: yulu
#     Update #: 598
# 


import numpy as np
import pandas
from scipy.integrate import quad
import os
import re

from SciBeam.core.common import Common
from SciBeam.core.regexp import RegExp    
from SciBeam.core import tofseries
from SciBeam.core import base
from SciBeam.core.descriptor import DescriptorMixin
from SciBeam.core import numerical

import matplotlib.pyplot as plt
from SciBeam.core.plotframe import PlotTOFFrame
    
class TOFFrame(pandas.DataFrame):
    
    """
    Single time-of-flight data analysis
    data: value of tof measure, shape(len(labels), len(times))
    time: time, 1D array of time for each tof data point
    label: label of the tof measurement, for mulitple same tof measurement 
           under different conditions, e.g. sensor position, etc. 
    time_unit: unit for time, optional, default None
    value_unit: unit for tof values, default None
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
    def fromtxt(cls, path, regStr, lowerBound = None, upperBound = None, removeOffset = True,
                offset_margin = 'both', offset_margin_size = 20,skiprows = 0, sep = '\t'):
        """
        Buid TOF instance from given file
        Current only works for '\t' seperated txt and lvm file
        """

        path = Common.winPathHandler(path)
        # If given folder path
        if os.path.isdir(path):
            if regStr:
                keys, files = RegExp.fileMatch(path, regStr)
                values = {}
                for k, f in zip(keys, files):
                    data = Common.loadFile(path + f, skiprows = skiprows, sep = sep)
                    if lowerBound and upperBound:
                        lb, ub = TOFFRAME.find_time_idx(data[:, 0], lowerBound, upperBound)
                        time = data[lb:ub, 0]
                        if removeOffset:
                            value = TOFFRAME.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, offset_margin = offset_margin, offset_margin_size = offset_margin_size)
                        else:
                            value = data[lb:ub, 1]
                    else:
                        time = data[:, 0]
                        value = data[:, 1]
                    values[k] =  value
            
            else:
                raise ValueError("[*] Please provide regStr for file match in the path !")

        # if given file path
        else:
            data = Common.loadFile(path, cols = cols, usecols = usecols,skiprows = skiprows,  sep = sep)
            if lowerBound and upperBound:
                lb, ub = TOFFRAME.find_time_idx(data[:,0], lowerbound, upperBound)
                time = data[lb : ub, 0]
                if removeOffset:
                    value = TOFFRAME.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, offset_margin = offset_margin, offset_margin_size = offset_margin_size)
                else:
                    value = data[lb:ub, 1]
            else:
                time = data[:,0]
                value = data[:,1]
            values = dict('value', value)
            
        return cls(values, index = time)
            

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
    def peakHeight(self, gauss_fit = False, offset = False):
        """
        peakHeight
        find peak height from dataframe
        --------------------
        return series
        """
        
        return self.apply(tofseries.TOFSeries.height, gauss_fit = gauss_fit, offset = offset)
        
    @_toTOFSeries
    def peakTime(self, gauss_fit = False):
        """
        peakTime
        find peak arrival time 
        ----------------------
        return series
        """
        return self.apply(tofseries.TOFSeries.peakTime, gauss_fit = gauss_fit)
        
    @_toTOFSeries
    def peakArea(self, gauss_fit = False):
        """
        peakArea
        find peak integrated signal(area)
        ---------------------
        return series
        """
        
        return  self.apply(tofseries.TOFSeries.area, gauss_fit = gauss_fit)
            
    @_toTOFSeries
    def peakFWHM(self, gauss_fit = True):
        """
        peakFWHM
        find peak FWHM
        ---------------------
        return series
        """
        return self.apply(tofseries.TOFSeries.fwhm,  gauss_fit = gauss_fit)

    @_toTOFFrame
    def selectPeakRegion(self, n_sigmas = 2, lowerBound = None, upperBound = None, as_frame = False, as_bounds = False, as_figure = True, inplace = False):
        """
        Automatically detect and select peak region
        """
        lowerBoundIdx = []
        upperBoundIdx = []
        for col in self.columns:
            lb, ub = self[col].peakFinder(as_bounds = True, n_sigmas = n_sigmas, lowerBound = lowerBound, upperBound = upperBound)
            lowerBoundIdx.append(lb)
            upperBoundIdx.append(ub)
        lowerBoundIdx = int(np.mean(lowerBoundIdx))
        upperBoundIdx = int(np.mean(upperBoundIdx))

        if as_figure:
            if len(self.columns) > 1:
                plt.imshow(self.iloc[lowerBoundIdx : upperBoundIdx, :].T, aspect = 'auto')
            else:
                self.iloc[lb:ub,:].plot(use_index = True, title = 'selectPeakRegion result')

        elif as_bounds:
            return lowerBoundIdx, upperBoundIdx
        elif as_frame:
            if inplace:
                self.__init__(self.iloc[lowerBoundIdx : upperBoundIdx, :])
            else:
                return self.iloc[lowerBoundIdx : upperBoundIdx, :]
        else:
            raise ValueError("[*] Please specify return method: as_bounds, as_frame, as_figure")
    
    def inch_to_mm(self, offset_inch = 0, inplace = False):
        """
        convert inches to milimeters in the columns names
        """
        values = (self.columns -  offset_inch) * 25.4
        if inplace:
            self.columns = values
        else:
            return values

    def mm_to_inch(self, offset_mm = 0, inplace = False):
        """
        convert milimeters to inches in the columns names
        """
        values = (self.columns -  offset_mm) /  25.4
        if inplace:
            self.columns = values
        else:
            return values

    def sec_to_microsec(self, offset_sec = 0, inplace = False):
        """
        convert seconds in index to microseconds
        """
        times = (self.index - offset_sec) * 1e6
        if inplace:
            self.index = times
        else:
            return times

    def microsec_to_sec(self, offset_microsec = 0, inplace = False):
        """
        convert microseconds in index to seconds
        """
        times = (self.index - offset_microsec) * 1e-6
        if inplace:
            self.index = times
        else:
            return times

    
    
    #Descriptors:
    #single = DescriptorMixin(TimeSeries)
    Plot = DescriptorMixin(PlotTOFFrame)

    
