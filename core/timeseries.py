# TimeSeries.py --- 
# 
# Filename: TimeSeries.py
# Description: 
#            Class TimeSeries
#            ------------------
#            Data analysis for time series for time series
#            data
#
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri Mar 23 23:09:44 2018 (-0500)
# Version: 0.1
# Last-Updated: Wed May  9 11:30:28 2018 (-0500)
#           By: yulu
#     Update #: 212
# 

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import quad
import matplotlib.pyplot as plt

from SciBeam.core import base


class TimeSeries:
    """
    pandas Series  based analysis on time series measurement
    
    """
    
    def __init__(self, data):
        self.__is_mixin = base._is_mixin(data)
        self.data = data._make_mixin if self.__is_mixin else data
        self.time = np.array(self.__data.index)
        self.value  = np.array(self.__data.values)
        
    @classmethod
    def _make_descriptor(cls,data):
        """
        Make class object for descriptor 
        """
        return cls(data)
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        """
        Set data value according to the passed data format
        Works for 2D array, list of arrays, pands.Series
        Time has to be the 0th column, data in other columns 
        """
                
        if data is None:
            self.__data = pd.Series()
            print("[*] Warning:Empty time series frame created !")
            
        elif type(data) is np.ndarray:
            if data.ndim  == 2:
                if data.shape[0] == 2:
                    t = data[0, :]
                    d = data[1, :]
                elif data.shape[1] == 2:
                    t = data[:,0]
                    d = data[:,1]
                else:
                    print("[*] Too many rows / columns for building a Series")
                    print("[!] Please make sure array is [2 X n] of [n x 2] with time being the first row / column")
                    raise ValueError
                self.__data = pd.Series(d, index = t)
            elif data.ndim == 1:
                self.__data = pd.Series(d, index = np.arange(len(d)))
                print("[*] No time value setted due to the given 1D array")
                print("[!] Please set time value by TimeSeries.data.index = ...")
            else:
                raise ValueError("\n[*] Cannot convert data to Series")
        
        elif type(data) is pd.core.series.Series:
            self.__data = data
            
        else:
            print("[*] Input data not understood !")
            print("Data should be one of the below:\n" + 
                  "o pandas Series with time as the index\n" + 
                  "o [2 X n] or [n X 2] array with time as 0th row / column")

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
                if abs(t - time[candi_idx]) > t_max_gap:
                        raise ValueError("[*] Error: find_time_idx didn't find closest match !\n" + 
                                         "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                                         %(t, time[candi_idx]))
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
        slice_t = []
        slice_value = []
        for arg_elem in self.find_time_idx(self.time, args):
            if hasattr(arg_elem, '__iter__'):
                for t in arg_elem:
                    slice_t.append(self.time[t])
                    slice_vlaue.append(self.data.iloc[t])
            else:
                slice_t.append(self.time[arg_elem])
                slice_value.append(self.data.iloc[arg_elem])
        slice_series = pd.Series(slice_value, index = slice_t)
                
        return slice_series

    def selectTimeRange(self, lowerBound, upperBound):
        """
        makeTimeRange
        Select continious data in a provided time range
        --------------
        """
        lb, ub = self.find_time_idx(self.time, lowerBound, upperBound)
        return self.data[lb:ub].copy() # Series
        

    def peakFinder(self, n_simgas = 4, as_bounds = True, as_series = False, as_figure = False, removeOffset = True, lowerBound = None, upperBound = None):
        if lowerBound or upperBound:
            series = self.selectTimeRange(lowerBound, upperBound)
        else:
            series = self.data.copy()
        if removeOffset:
            series = self.__remove_margin_offset(series)
        peak_idx = np.argmax(series.value)
        peak_value = series.value[peak_idx]
        half_max = peak_value / 2.
        hwhm_idx_left = np.argmin(abs(series.value[:peak_idx] - half_max))
        delta_idx = int((peak_idx - hwhm_idx_left) / (2.355 / 2) * n_simgas / 2 )
        lb,ub  = peak_idx - delta_idx, peak_idx + delta_idx
        if as_bounds:
            return lb, ub 
        elif as_series:
            return series[lb:ub]
        elif as_figure:
            plt.figure()
            series.plot()
            plt.xlabel('time')
            plt.ylabel('value')
            plt.title('Peak finder result')
            plt.show()
        else:
            raise ValueError("[*] Please specify return method: as_bounds, as_series, as_figure")
            
        
    @staticmethod
    def __remove_margin_offset(data, n_margin = 5, how = 'both'):
        """
        remove offset based on the mean values on the margin of givine data values
        """
        if data.ndim == 1:
            if len(data) < 10 * n_margin:
                raise IndexError("[*]Data range too small to perform margin offfset removal!")
            elif how == 'both':
                margin_offset = (data[:5].mean() + data[-5:].mean()) / 2
            elif how == 'left':
                margin_offset = data[:5].mean()
            elif how == 'right':
                margin_offset = data[-5:].mean()
            else:
                raise ValueError("[*] how = %s not understand: acceptable values are ['both', 'left', 'right']" %how)
            result = data - margin_offset
        else:
            raise ValueError("[*] data not understand, only acceptable 1D array or pandas Series")
        return result
        
        
    @property
    def describe(self):
        return self.data.describe()

    
    # @staticmethod
    # def gaus0(x, *args):
    #     """
    #     Gaussian function with 0 offset
    #     """
        
    #     return args[0] * np.exp(- (x - args[1])**2 / (2 * args[2]**2))

    # @staticmethod
    # def gaus(x, *args):
    #     """
    #     Gaussian function with offset
    #     """
    #     return args[0] * np.exp(- (x - args[1])**2 / (2 * args[2]**2)) + args[3]
    
    # @staticmethod
    # def gausFit(x, y, plot=False):
    #     idxMax = np.argmax(y)
    #     a0 = y[idxMax]
    #     x0 = x[idxMax]
    #     halfWidth = x[idxMax + np.argmin(abs(y[idxMax:] - a0 / 2))] - x[idxMax]
    #     popt, pcov = curve_fit(TimeSeries.gaus0, xdata = x, ydata = y, p0 = [a0, x0, halfWidth])
        
    #     if plot:
    #         fig, ax = plt.subplots(figsize = (8,5))
    #         ax.plot(x, y, 'o', label = 'raw data')
    #         if len(x) < 10:
    #             xEval = np.linspace(min(x), max(x), 10 * len(x))
    #         else:
    #             xEval = x
    #         ax.plot(xEval, TimeSeries.gaus0(xEval, *popt), '--', label = 'gaussian fitting')
    #         ax.set_xlabel('X')
    #         ax.set_ylabel('Y')
    #         ax.set_title('Gaussian fitting on X and Y')
    #         plt.show()
    #     else:
    #         pass
    #     popt[2] = abs(popt[2]) # sigma only takes positive value
    #     return (popt, pcov)

    
    # def peakHeight(self, fit = False, error = False):
    #     if type(self.data) is pd.core.frame.DataFrame:
    #         data = self.data.values
            
    #     try:
    #         nRow, nCol = self.__data.shape
    #     except AttributeError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise AttributeError
    #     except ValueError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise ValueError
    #     else:
    #         if fit:
    #             fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
    #             peak, peakErr = np.array([[x[0][0], np.sqrt(x[1][0, 0])] for x in fitRes]).T
    #         else:
    #             peak = [max(k) for k in data[:, 1:].T]
    #     finally:            
    #         peak = peak[0] if len(peak) == 1 else peak               
    #         if fit and error:                
    #             peakErr = peakErr[0] if len(peakErr) == 1 else peakErr
    #             return(peak, peakErr)
    #         else:
    #             return(peak)
        
    # def peakTime(self, fit = False, error = False):
    #     if type(self.data) is pd.core.frame.DataFrame:
    #         data = self.data.values
    #     try:
    #         nRow, nCol = data.shape
    #     except AttributeError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise AttributeError
    #     except ValueError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise ValueError
    #     else:
    #         if fit:
    #             fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
    #             peakTime, peakTimeErr = np.array([[x[0][1], np.sqrt(x[1][1, 1])] for x in fitRes]).T
    #         else:
    #             peakTime = [data[np.argmax(k), 0] for k in data[:, 1:].T]
    #     finally:            
    #         peakTime = peakTime[0] if len(peakTime) == 1 else peakTime               
    #         if fit and error:                
    #             peakTimeErr = peakTimeErr[0] if len(peakTimeErr) == 1 else peakTimeErr
    #             return(peakTime, peakTimeErr)
    #         else:
    #             return(peakTime)
        
    # def peakFWHM(self, fit = False, error = False):
    #     if type(self.data) is pd.core.frame.DataFrame:
    #         data = self.data.values
    #     try:
    #         nRow, nCol = data.shape
    #     except AttributeError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise AttributeError
    #     except ValueError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise ValueError
    #     else:
    #         if fit:
    #             fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
    #             peakFWHM, peakFWHMErr = np.array([[x[0][2], np.sqrt(x[1][2, 2])] for x in fitRes]).T
    #         else:
    #             peakFWHM = []
    #             for dataY in data[:,1:].T:
    #                 maxIdx = np.argmax(dataY)
    #                 peak = dataY[maxIdx]
    #                 idxLow = np.argmin(np.abs(dataY[:maxIdx] - peak/2.))
    #                 idxHigh = np.argmin(np.abs(dataY[maxIdx:] - peak/2.)) + maxIdx
    #                 peakFWHM.append(data[idxHigh, 0] - data[idxLow, 0])
    #     finally:         
    #         peakFWHM = peakFWHM[0] if len(peakFWHM) == 1 else peakFWHM               
    #         if fit and error:                
    #             peakFWHMErr = peakFWHMErr[0] if len(peakFWHMErr) == 1 else peakFWHMErr
    #             return(peakFWHM, peakFWHM)
    #         else:
    #             return(peakFWHM)
            
    # def peakIntegrate(self, fit = False, error = False):
    #     if type(self.data) is pd.core.frame.DataFrame:
    #         data = self.data.values
    #     try:
    #         nRow, nCol = data.shape
    #     except AttributeError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise AttributeError
    #     except ValueError:
    #         print("[!] Input data has to be 2D array with time series as 0th column!")
    #         raise ValueError
    #     else:
    #         if fit:
    #             popt = [self.gausFit(data[:,0], y)[0] for y in data[:,1:].T]
    #             # intergrate (-6sigma,6sigma) region 
    #             peakIntegrate, peakIntegrateErr = np.array([quad(TimeSeries.gaus0, y[1] - 6*y[2], y[1] + 6*y[2], args = tuple(y)) for y in popt]).T
                
    #         else:
    #             peakIntegrate = [np.trapz(x = data[:,0], y = s) for s in data[:,1:].T]
    #     finally:         
    #         peakIntegrate = peakIntegrate[0] if len(peakIntegrate) == 1 else peakIntegrate               
    #         if fit and error:                
    #             peakIntegrateErr = peakIntegrateErr[0] if len(peakIntegrateErr) == 1 else peakIntegrateErr
    #             return(peakIntegrate, peakIntegrate)
    #         else:
    #             return(peakIntegrate)

            
        
