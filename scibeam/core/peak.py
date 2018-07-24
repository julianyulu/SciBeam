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
# Last-Updated: Fri Jul 20 23:37:45 2018 (-0500)
#           By: yulu
#     Update #: 251
# 


import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

import SciBeam
from SciBeam.core import base
from SciBeam.core.gaussian import Gaussian
from SciBeam.core import tofseries


__all__ = [
    'SeriesPeak',
    'FramePeak',
    ]

class SeriesPeak(pandas.Series):
    """
    Peak analysis on 1D labeled / unlabeled data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    @classmethod
    def _constructor(cls, *args, **kwargs):
        return cls(*args, **kwargs)


    def gausFit(self, plot = False):
        popt, pcov = Gaussian.gausFit(x = self.index, y = self.values, offset = False, plot = plot)
        return popt, pcov
    
    def idx(self, gauss_fit = False):
        if gauss_fit:
            return self.gausFit()[0][1]
        else:
            return self.idxmax()

    def nidx(self, gauss_fit = False):
        if gauss_fit:
            height = self.height(gauss_fit)
            nidx = np.argmin(abs(self.values - height))
        else:
            nidx = np.argmax(self.values)
        return nidx
        
    def height(self, gauss_fit = False):
        if gauss_fit:
            return self.gausFit()[0][0]
        else:
            return self.max()
        
    def sigma(self, n_sigmas = 1, gauss_fit = False):
        if gauss_fit:
            return self.gausFit()[0][2]
        else:
            peak_values = max(self)
            peak_idx = np.argmax(self.values)
            half_max = peak_values / 2
            hwhm_idx_left = np.argmin(abs(self.iloc[:peak_idx] - half_max))
            hwhm_idx_right = np.argmin(abs(self.iloc[peak_idx : ] - half_max)) + peak_idx
            fwhm = self.index[hwhm_idx_right] - self.index[hwhm_idx_left]
            sigma = fwhm / np.sqrt(8*np.log(2))
            return sigma * n_sigmas

    def fwhm(self, gauss_fit = False):
        sigma = self.sigma(n_sigmas = 1, gauss_fit = gauss_fit)
        return sigma * np.sqrt(8 * np.log(2))

    def area(self, gauss_fit = False):
        if gauss_fit:
            popt, pcov = self.gausFit()
            # if with offset 
            #area = quad(lambda x:Gaussian.gaus(x, *popt) - popt[-1], min(data_label), max(data_label))[0]
            # assume no offset
            area = quad(lambda x:Gaussian.gaus(x, *popt), min(self.index), max(self.index))[0]
        else:
            # if with offset
            # area = np.trapz(x = data_label, y = self - np.min(self))
            
            # assume no offset
            area = np.trapz(x = self.index, y = self.values)
        return area

    def region(self, n_sigmas = 4, plot = False):
        """
        Locate the region where there exists a peak
        return the bound index of the region
        """
        peak_nidx = self.nidx()
        peak_value = self.iloc[peak_nidx]
        
        hwhm_nidx_left = peak_nidx - np.argmin(abs(self.iloc[peak_nidx:0:-1].values - peak_value / 2))
        hwhm_nidx_right = np.argmin(abs(self.iloc[peak_nidx:].values - peak_value / 2)) + peak_nidx
        fwhm_nidx_range = hwhm_nidx_right - hwhm_nidx_left
        
        delta_nidx = int(fwhm_nidx_range / np.sqrt(8 * np.log(2)) * n_sigmas)
        lb,ub  = peak_nidx - delta_nidx, peak_nidx + delta_nidx
        lb = 0 if lb < 0 else lb
        ub = len(self) if ub > len(self) else ub

        if plot:
            plt.plot(self.index, self.values, '--', label = 'raw input')
            plt.plot(self.index[lb:ub], self.values[lb:ub], '-', label = 'detected peak')
        return lb, ub 

    def autocrop(self, n_sigmas = 4):
        lb, ub =  self.region(n_sigmas = n_sigmas, plot = False)
        return self._constructor(self.iloc[lb:ub])




    

class FramePeak(pandas.DataFrame):
    """
    Peak analysis on 1D labeled / unlabeled data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    @classmethod
    def _constructor(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @_toTOFSeries
    def idx(self, gauss_fit = False):
        if gauss_fit:
            return self.apply(lambda s: Gaussian.gausFit(x = s.index, y = s.values, offset = False)[0][1])
        else:
            return self.idxmax()

    @_toTOFSeries
    def nidx(self, gauss_fit = False):
        if gauss_fit:
            height = self.height(gauss_fit)
            n_idx = [np.argmin(abs(self[x].values - h)) for x, h in zip(self.columns, height)]
        else:
            n_idx = [np.argmax(self[x].values) for x in self.columns]
        n_idx = pandas.Series(n_idx, self.columns)
        return n_idx

    @_toTOFSeries
    def height(self, gauss_fit = False):
        if gauss_fit:
            return self.apply(lambda s: Gaussian.gausFit(x = s.index, y = s.values, offset = False)[0][0])
        else:
            return self.max()

    @_toTOFSeries
    def sigma(self, n_sigmas = 1, gauss_fit = False):
        
        def col_sigma(series):
            if gauss_fit:
                return series.gausFit()[0][2]
            else:
                peak_values = max(series)
                peak_idx = np.argmax(series.values)
                half_max = peak_values / 2
                hwhm_idx_left = np.argmin(abs(series.iloc[:peak_idx].values - half_max))
                hwhm_idx_right = np.argmin(abs(series.iloc[peak_idx : ].values - half_max)) + peak_idx
                fwhm = series.index[hwhm_idx_right] - series.index[hwhm_idx_left]
                sigma = fwhm / np.sqrt(8*np.log(2))
            return sigma * n_sigmas
        
        return self.apply(col_sigma)
        
    @_toTOFSeries
    def fwhm(self, gauss_fit = False):
        sigma = self.sigma(n_sigmas = 1, gauss_fit = gauss_fit)
        return sigma * np.sqrt(8 * np.log(2))

    @_toTOFSeries
    def area(self, gauss_fit = False):
        def col_area(series):
            if gauss_fit:
                for col in series.columns:
                    popt, pcov = series[col].gausFit()
                    area = quad(lambda x:Gaussian.gaus(x, *popt), min(series[col].index), max(series[col].index))[0]
                           
            else:
                area = np.trapz(x = series.index, y = series.values)
            return area
        return self.apply(col_area)

    @_toTOFSeries
    def region(self, n_sigmas = 4, plot = False):
        """
        Locate the region where there exists a peak
        return the bound index of the region
        """
        def col_region(series):
            series = SeriesPeak(series.copy())
            peak_nidx = series.nidx()
            peak_value = series.iloc[peak_nidx]
        
            hwhm_nidx_left = peak_nidx - np.argmin(abs(series.iloc[peak_nidx:0:-1].values - peak_value / 2))
            hwhm_nidx_right = np.argmin(abs(series.iloc[peak_nidx:].values - peak_value / 2)) + peak_nidx
            fwhm_nidx_range = hwhm_nidx_right - hwhm_nidx_left
        
            delta_nidx = int(fwhm_nidx_range / np.sqrt(8 * np.log(2)) * n_sigmas)
            lb,ub  = peak_nidx - delta_nidx, peak_nidx + delta_nidx
            lb = 0 if lb < 0 else lb
            ub = len(series) if ub > len(series) else ub

            if plot:
                plt.plot(series.index, series.values, '--', label = 'raw input')
                plt.plot(series.index[lb:ub], series.values[lb:ub], '-', label = 'detected peak')
            return lb, ub
        
        return self.apply(col_region)

    


