# tofseries.py --- 
# 
# Filename: tofseries.py
# Description: 
#            single time-of-flight data series analysis
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri May  4 10:53:40 2018 (-0500)
# Version: 
# Last-Updated: Sun May 13 16:16:19 2018 (-0500)
#           By: yulu
#     Update #: 624
# 


import numpy as np
import pandas
from scipy.integrate import quad
import os
import re

from SciBeam.core.descriptor import DescriptorMixin
from SciBeam.core.common import Common
from SciBeam.core.regexp import RegExp    
from SciBeam.core import base
from SciBeam.core import numerical
from SciBeam.core import tofframe
from SciBeam.core.plotseries import PlotTOFSeries

class TOFSeries(pandas.Series):
    pandas.set_option('precision', 9)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @property
    def _constructor(self):
        return TOFSeries
    @property
    def _constructor_expanddim(self):
        return tofframe.TOFFrame
    
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
                return TOFSeries(result)
            else:
                return result
        return wrapper
    
    @classmethod
    def fromtxt(cls, path, regStr, lowerBound = None, upperBound = None, removeOffset = True,
                offset_margin = 'outer', offset_margin_size = 20,skiprows = 0, sep = '\t'):
        """
        Buid TOF instance from given file
        Current only works for '\t' seperated txt and lvm file
        """

        path = Common.winPathHandler(path)
        # If given folder path
        if os.path.isdir(path):
            raise ValueError("[*] TOFSeries only take single file as series source!")

        # if given file path
        else:
            data = Common.loadFile(path, cols = cols, usecols = usecols,skiprows = skiprows,  sep = sep)
            if lowerBound and upperBound:
                lb, ub = TOFSeries.find_time_idx(data[:,0], lowerbound, upperBound)
                time = data[lb : ub, 0]
                if removeOffset:
                    value = TOFSeries.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, offset_margin = offset_margin, offset_margin_size = offset_margin_size)
                else:
                    value = data[lb:ub, 1]
            else:
                time = data[:,0]
                value = data[:,1]
        return cls(values, index = time)
    

    def height(self, gauss_fit = False, offset = False):
        """
        peakHeight
        find peak height from dataframe
        --------------------
        return series
        """
        if gauss_fit:
            return numerical.gausFit(x = self.index, y = self.values, offset = offset)[0][0]
        else:
            return self.max()
        
    def peakTime(self, gauss_fit = False):
        """
        peakTime
        find peak arrival time 
        ----------------------
        return series
        """
        if gauss_fit:
            return numerical.gausFit(x = self.index, y = self.values, offset = False)[0][1]
        else:
            return self.idxmax()

    def area(self, gauss_fit = False):
        """
        integrated signal area
        if gauss_fit is True, return area on fitted signal
        else return normal numerically integrated signal
        """
        if gauss_fit:
            popt, pcov = numerical.gausFit(x = self.index, y = self.values, offset = False)
            area = quad(lambda x:numerical.gaus(x, *popt), self.index.min(), self.index.max())[0]
        else:
            area = np.trapz(x = self.index, y = self.values)
        return area

    def fwhm(self, gauss_fit = True):
        """
        find fwhm, if gauss_fit == True(default), using gauss fit fwhm
        else use literally caculated fwhm
        """
        if gauss_fit:
            popt, pcov = numerical.gausFit(x = self.index, y = self.values, offset = False)
            fwhm = np.sqrt(2 * np.log(2)) * abs(popt[2])
        else:
            time = self.index
            value = self.values
            peak_values = max(value)
            peak_idx = np.argmax(value)
            half_max = peak_values / 2
            hwhm_idx_left = np.argmin(abs(value[:peak_idx] - half_max))
            hwhm_idx_right = np.argmin(abs(value[peak_idx : ] - half_max)) + peak_idx
            fwhm = time[hwhm_idx_right] - time[hwhm_idx_left]
        return fwhm

    

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

    @_toTOFSeries
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
        slice_series = pandas.Series(slice_value)
        if inplace:
            self.__init__(slice_series)
        else:
            return slice_series

    @_toTOFSeries
    def selectTimeRange(self, lowerBound, upperBound, inplace = False):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = TOFSeries.find_time_idx(self.index, lowerBound, upperBound)
        selected = self.iloc[lb:ub, :].copy()
        if inplace:
            self.__init__(selected)
        else:
            return selected

    @_toTOFSeries
    def peakFinder(self, n_sigmas = 2, as_bounds = True, as_series = False, as_figure = False, removeOffset = False, lowerBound = None, upperBound = None):
        if lowerBound or upperBound:
            lb, ub = TOFSeries.find_time_idx(self.index, lowerBound, upperBound)
            data = self.iloc[lb:ub, :].copy()
        else:
            data = self.copy()

        time = data.index
        value = data.values
        
        if removeOffset:
            value = TOFSeries.remove_data_offset(value, how = 'inner', margin_size = 5)
        else:
            pass
        
        peak_idx = np.argmax(value)
        peak_value = value[peak_idx]
        
        hwhm_idx_left = np.argmin(abs(value[:peak_idx] - peak_value / 2))
        hwhm_idx_right = np.argmin(abs(value[peak_idx:] - peak_value / 2)) + peak_idx
        fwhm_index_range = hwhm_idx_right - hwhm_idx_left
        ## This is the "index" of dataframe not index like 1,2,3,4, doesn't work
        delta_idx = int(fwhm_index_range / np.sqrt(8 * np.log(2)) * n_sigmas)
        lb,ub  = peak_idx - delta_idx, peak_idx + delta_idx
        lb = 0 if lb < 0 else lb
        ub = len(value) if ub > len(value) else ub
        
        if as_figure:
            self.iloc[lb:ub].plot(use_index = True, title = 'peakFinder result')
        else:
            pass
        if as_series:
            return self[lb:ub]
        elif as_bounds:
            return lb, ub 
        else:
            raise ValueError("[*] Please specify return method: as_bounds, as_series, as_figure")

        
    def selectPeakRegion(self, inplace = False, plot = False):
        """
        auto select peak region
        """
        if plot:
            if inplace:
                series = self.peakFinder(as_series = True, as_figure =True)
                self.__init__(self.peakFinder(as_series = True))
            else:
                self.peakFinder(as_bounds = False, as_figure =True)
        else:
            if inplace:
                self.__init__(self.peakFinder(as_series = True))
            else:
                return self.peakFinder(as_series = True)

    def sec_to_microsec(self, offset_sec = 0, inplace = False):
        """
        convert seconds in index to microseconds
        """
        times = (self.index - offset_sec) * 1e6
        if inplace:
            self.index = times
        else:
            return times

    # Descriptors
    plot1d = DescriptorMixin(PlotTOFSeries)
