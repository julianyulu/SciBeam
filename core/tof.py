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
# Last-Updated: Sat May 12 12:26:09 2018 (-0500)
#           By: yulu
#     Update #: 470
# 


import numpy as np
import pandas as pd
from scipy.integrate import quad
import os
import re

from SciBeam.core.common import Common
from SciBeam.core.regexp import RegExp    
#from SciBeam.core.timeseries import TimeSeries
from SciBeam.core import base
from SciBeam.core.descriptor import DescriptorMixin
from SciBeam.core import numerical

#from SciBeam.core.plot import Plot

class TOFSeries(pd.Series):
    @property
    def _constructor(self):
        return TOFSeries
    @property
    def _constructor_expanddim(self):
        return TOF

class TOF(pd.DataFrame):
    
    """
    Single time-of-flight data analysis
    data: value of tof measure, shape(len(labels), len(times))
    time: time, 1D array of time for each tof data point
    label: label of the tof measurement, for mulitple same tof measurement 
           under different conditions, e.g. sensor position, etc. 
    time_unit: unit for time, optional, default None
    value_unit: unit for tof values, default None
    """
    pd.set_option('precision', 9)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    @property
    def _constructor(self):
        return TOF
    @property
    def _constructor_sliced(self):
        return TOFSeries

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
                        lb, ub = TOF.find_time_idx(data[:, 0], lowerBound, upperBound)
                        time = data[lb:ub, 0]
                        if removeOffset:
                            value = TOF.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, offset_margin = offset_margin, offset_margin_size = offset_margin_size)
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
                lb, ub = TOF.find_time_idx(data[:,0], lowerbound, upperBound)
                time = data[lb : ub, 0]
                if removeOffset:
                    value = TOF.remove_data_offset(data[:, 1], lowerBoundIdx = lb, upperBoundIdx = ub, offset_margin = offset_margin, offset_margin_size = offset_margin_size)
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
    def remove_data_offset(data, lowerBoundIdx = None, upperBoundIdx = None, offset_margin = 'both', offset_margin_size = 10):
        """
        remove offset in 1D array data
        """
        if offset_margin == 'both':
            offset = (np.mean(data[lowerBoundIdx-offset_margin_size: lowerBoundIdx]) + np.mean(data[upperBoundIdx : upperBoundIdx + offset_margin_size]))  / 2.
        elif offset_margin == 'left':
            offset = np.mean(data[lowerBoundIdx-offset_margin_size: lowerBoundIdx])
        elif offset_margin == 'right':
            offset = np.mean(data[upperBoundIdx : upperBoundIdx + offset_margin_size])
        elif offset_margin == 'inner':
            offset = (np.mean(data[lowerBoundIdx: lowerBoundIdx + offset_margin_size]) + np.mean(data[upperBoundIdx - offset_margin_size: upperBoundIdx]))  / 2
        elif offset_margin == 'inner left':
            offset = np.mean(data[lowerBoundIdx: lowerBoundIdx + offset_margin_size])
        elif offset_margin == 'inner right':
            offset = np.mean(data[upperBoundIdx - offset_margin_size: upperBoundIdx])
        else:
            raise ValueError(("[*] offset_margin: %s not understood !\n" +
                              "[!] possible values of offset_margin: 'both', 'left', 'right', 'inner', 'inner left', 'inner right'") % offset_margin)
        data = data[lowerBoundIdx:upperBoundIdx] - offset
        return data
    
                
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
        slice_DataFrame = pd.DataFrame(slice_value)
        if inplace:
            self.__init__(slice_DataFrame)
        else:
            return slice_DataFrame

    
    def selectTimeRange(self, lowerBound, upperBound, inplace = False):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = TOF.find_time_idx(self.index, lowerBound, upperBound)
        selected = self.iloc[lb:ub, :].copy()
        if inplace:
            self.__init__(selected)
        else:
            return selected
        

    
    def peakHeight(self, gauss_fit = False, offset = False):
        """
        peakHeight
        find peak height from dataframe
        --------------------
        return series
        """
        if gauss_fit:
            return  self.apply(lambda z: numerical.gausFit(x = z.index, y = z.values, offset = offset)[0][0])
            
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
            return  self.apply(lambda z: numerical.gausFit(x = z.index, y = z.values, offset = False)[0][1])
        else:
            return self.idxmax()
        
    def peakArea(self, gauss_fit = False):
        """
        peakArea
        find peak integrated signal(area)
        ---------------------
        return series
        """
        def integ_gaus_area(series):
            popt, pcov = numerical.gausFit(x = series.index, y = series.values, offset = False)
            area = quad(lambda x:numerical.gaus(x, *popt), series.index.min(), series.index.max())[0]
            return area
        
        if gauss_fit:
            return  self.apply(integ_gaus_area)
        else:
            return self.apply(lambda z: np.trapz(x = z.index, y = z.values))
    

    def peakFWHM(self, gauss_fit = True):
        """
        peakFWHM
        find peak FWHM
        ---------------------
        return series
        """
        def gaus_fit_fwhm(series):
            popt, pcov = numerical.gausFit(x = series.index, y = series.values, offset = False)
            fwhm = np.sqrt(2 * np.log(2)) * abs(popt[2])
            return fwhm

        def literal_fwhm(series):
            time = series.index
            value = series.values
            peak_values = max(value)
            peak_idx = np.argmax(value)
            half_max = peak_values / 2
            hwhm_idx_left = np.argmin(abs(value[:peak_idx] - half_max))
            hwhm_idx_right = np.argmin(abs(value[peak_idx : ] - half_max)) + peak_idx
            fwhm = time[hwhm_idx_right] - time[hwhm_idx_left]
            return fwhm
        
        if gauss_fit:
            return  self.apply(gaus_fit_fwhm)
        
        else:
            return self.apply(literal_fwhm)
        

    def inch_to_mm(self, offset_inch = 0, inplace = False):
        """
        convert inches to milimeters in the columns names
        """
        values = (self.columns -  offset_inch) * 25.4
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
        
        
    '''
    
    def peakFinder(self, n_simgas = 4, as_bounds = True, as_series = False, as_figure = False, removeOffset = True, lowerBound = None, upperBound = None):
        if lowerBound or upperBound:
            lb, ub = TOF.find_time_idx(self.index, lowerBound, upperBound)
            data = self.iloc[lb:ub, :]
        else:
            data = self
        if removeOffset:
            data = TOF.remove_data_offset(data, offset_margin = 'inner', offset_margin_size = 5)
        peak_idx = self.idxmax()
        hwhm_idx_left = self.apply(lambda x: pd.Series.idxmin(abs(x[:pd.Series.idxmax(x)] - x.max() / 2)))
        ## This is the "index" of dataframe not index like 1,2,3,4, doesn't work
        delta_idx = (peak_idx - hwhm_idx_left) / (2.355 / 2) * n_simgas / 2
        lb,ub  = peak_idx - delta_idx, peak_idx + delta_idx
        if as_bounds:
            return lb, ub 
        elif as_series:
            return [self.loc[lb.iloc[i]:ub.iloc[i], self.columns[i]] for i in range(len(lb))]
        elif as_figure:
            plt.figure()
            series.plot()
            plt.xlabel('time')
            plt.ylabel('value')
            plt.title('Peak finder result')
            plt.show()
        else:
            raise ValueError("[*] Please specify return method: as_bounds, as_series, as_figure")
    '''

    
    # #Descriptors:
    # #single = DescriptorMixin(TimeSeries)
    # plot = DescriptorMixin(Plot)

    
# Class Tof end <---
