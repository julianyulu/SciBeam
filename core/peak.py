# peak.py --- 
# 
# Filename: peak.py
# Description: 
#            peak analysis
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue Jun 26 16:50:12 2018 (-0500)
# Version: 
# Last-Updated: Mon Jul  9 19:19:28 2018 (-0500)
#           By: yulu
#     Update #: 106
# 


import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

import SciBeam
from SciBeam.core import base
from SciBeam.core.gaussian import Gaussian

class Peak:
    """
    Peak analysis in 1D / 2D data
    """

    def __init__(self, data, data_label = None):
        self._is_mixin = base._is_mixin(data)
        self.data = data._make_mixin if self._is_mixin else data
        if type(data) in [pandas.core.series.Series, SciBeam.core.tofseries.TOFSeries]:
        
            self._data_label = list(data.index)
        elif type(data) == pandas.core.frame.DataFrame:
            self._data_label = [list(data.index), list(data.columns)]
        else:
            self.data_label = data_label

    def _only_for_1D(func):
        """
        Decorator that limits some functions to be only used for 1D data
        """
        def wrapper(*args, **kwargs):
            if args[0]._ndim == 2:
                raise ValueError("Currently this function can only be applied to 1D data")
            else:
                return func(*args, **kwargs)
        return wrapper
    
    @classmethod
    def _constructor(cls, data):
        return cls(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        # Iterable input (lists, tuple, ...)
        if hasattr(data, '__iter__'):
            # 2D list
            self._data = np.array(data)
        elif type(data) in [np.ndarray,
                            pandas.core.series.Series,
                            pandas.core.frame.DataFrame]:
            self._data = data
        else:
            raise TypeError("Input data type {} not accepted".format(type(data)))
        
        self._shape = self._data.shape
        self._ndim = np.ndim(self._data)
        
        # Currently can noly handle 1D/2D data
        if self._ndim > 2:
                raise ValueError("*Peak* cannot handle data larger than 2D, input data has dimention {}".format(self._ndim))
        else:
            pass

    @property
    def data_label(self):
        return self._data_label

    @data_label.setter
    def data_label(self, data_label):
        if not data_label is None:
            if hasattr(data_label[0], '__iter__') and len(data) == 2:
                assert(data_label[0] == self._shape[0])
                assert(data_label[1] == self._shape[1])
                label = data_label
            elif len(data_label) == self._shape[0]:
                label = data_label
            else:
                raise ValueError("data_label dimention doesn't match data dimention")
        # elif type(self._data) == pandas.core.series.Series:
        #     label = np.array(self.index)
        # elif type(self._data) == pandas.core.frame.DataFrame:
        #     label = [np.array(self.index), np.array(self.columns)]
        elif self._ndim == 1:
            label = np.arange(self._shape[0])
        else:
            label = [np.arange(x) for x in self._shape]

        self._data_label = label

    @_only_for_1D
    def peakRegion(self, n_sigmas = 4, plot = False):
        """
        Locate the region where there exists a peak
        return the bound index of the region
        """
        peak_idx = self.peakIndex()
        peak_value = self._data[peak_idx]
        
        hwhm_idx_left = np.argmin(abs(self._data[:peak_idx] - peak_value / 2))
        hwhm_idx_right = np.argmin(abs(self._data[peak_idx:] - peak_value / 2)) + peak_idx
        fwhm_index_range = hwhm_idx_right - hwhm_idx_left
        
        delta_idx = int(fwhm_index_range / np.sqrt(8 * np.log(2)) * n_sigmas)
        lb,ub  = peak_idx - delta_idx, peak_idx + delta_idx
        lb = 0 if lb < 0 else lb
        ub = len(self._data) if ub > len(self._data) else ub

        if plot:
            plt.plot(self._data_label, self._data, '--', label = 'raw input')
            plt.plot(self._data_label[lb:ub], self._data[lb:ub], '-', label = 'detected peak')
            
        return lb, ub 
            
    def peakIndex(self):
        """
        find index that corresponds to peak value
        """
        if self._ndim == 1:
            idx = np.argmax(self._data)
        else:
            idxmax = np.argmax(self._data)
            idx = (idxmax // self._shape[1], idxmax % self._shape[1])
        return idx

    
    def peakValue(self, gauss_fit = False, data_label = None, offset = False):
        """
        Find peak value in give data
        Can use gaussian function fitting to find peak value 
        A seperate input for data label (e.g. x axis value) is optional
        """
        if gauss_fit:
            popt, pcov = self.gausFit(data_label = data_label, offset = offset)
            return popt[0]
        else:
            if offset:
                return np.max(self._data) - np.min(self._data)
            else:
                return np.max(self._data)
    

    
    def peakLabel(self, gauss_fit = False, data_label = None, offset = False):
        """
        Find corresponding label of the peak value in the given data
        Can use gaussian function fitting to find peak label
        A seperate input for data label (e.g. x axis value) is optional
        """
        data_label = data_label if not data_label is None else self._data_label
        if gauss_fit:
            popt, pcov = self.gausFit(data_label = data_label, offset = offset)
            return popt[1]
        else:
            if self._ndim == 1: # 1D data
                peak_label = data_label[self.peakIndex()]
                return peak_label
            else: # 2D data
                peak_label1 = data_label[0][self.peakIndex()[0]]
                peak_label2 = data_label[1][self.peakIndex()[1]]
                return (peak_label1, peak_label2)

    @_only_for_1D
    def gausFit(self, data_label = None, offset = False):
        """
        Fit data with gaussian function 
        """
        data_label = data_label if not data_label is None else self._data_label
        popt, pcov = Gaussian.gausFit(x = data_label, y = self.data,  offset = offset)
        return popt, pcov

    @_only_for_1D
    def peakArea(self, gauss_fit = False, data_label = None, offset = False):
        """
        Find integrated value of given data
        Can use gaussian function fitting to find area
        A seperate input for data label (e.g. x axis value) is optional
        """
        data_label = data_label if not data_label is None else self._data_label
        if gauss_fit:
            popt, pcov = self.gausFit(data_label = data_label, offset = offset)
            if offset: 
                area = quad(lambda x:Gaussian.gaus(x, *popt) - popt[-1], min(data_label), max(data_label))[0]
            else:
                area = quad(lambda x:Gaussian.gaus(x, *popt), min(data_label), max(data_label))[0]
        else:
            if offset:
                area = np.trapz(x = data_label, y = self._data - np.min(self._data))
            else:
                area = np.trapz(x = data_label, y = self._data)
            
        return area
    
    @_only_for_1D
    def peakFWHM(self, gauss_fit = False, data_label = None, offset = False):
        """
        Find peak Full-Width-Half-Maximium (FWHM)
        Can use gaussian function fitting to find fwhm
        A seperate input for data label (e.g. x axis value) is optional
        """
        data_label = data_label if not data_label is None else self._data_label
        if gauss_fit:
            popt, pcov = self.gausFit(data_label = data_label, offset = offset)
            return np.sqrt(8 * np.log(2)) * popt[2]
        else:
            peak_values = max(self._data)
            peak_idx = np.argmax(self._data)
            half_max = peak_values / 2
            hwhm_idx_left = np.argmin(abs(self._data[:peak_idx] - half_max))
            hwhm_idx_right = np.argmin(abs(self._data[peak_idx : ] - half_max)) + peak_idx
            fwhm = data_label[hwhm_idx_right] - data_label[hwhm_idx_left]
            return fwhm
