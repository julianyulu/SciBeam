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
# Last-Updated: Fri May 11 15:58:39 2018 (-0500)
#           By: superlu
#     Update #: 403
# 


import numpy as np
import pandas as pd
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
        for arg_elem in self.find_time_idx(self.index, args):
            if hasattr(arg_elem, '__iter__'):
                for t in arg_elem:
                    slice_value.append(self.iloc[t])
            else:
                slice_value.append(self.iloc[arg_elem])
        slice_DataFrame = pd.DataFrame(slice_value)
        return slice_DataFrame

    
    def selectTimeRange(self, lowerBound, upperBound):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = TOF.find_time_idx(self.index, lowerBound, upperBound)
        return self.iloc[lb:ub, :].copy()

    
    def peakHeight(self, gauss_fit = False, offset = False):\
        if gauss_fit:
            return  self.apply(lambda z: numerical.gausFit(x = z.index, y = z.values, offset = offset)[0][0])
            pass
        else:
            return self.max()
        
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
