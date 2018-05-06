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
# Last-Updated: Sun May  6 00:37:01 2018 (-0500)
#           By: yulu
#     Update #: 96
# 

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import quad
import matplotlib.pyplot as plt

from SciBeam.core import base


class TimeSeries:
    def __init__(self, data):
        self.__is_mixin = base._is_mixin(data)
        self.data = data._make_mixin if self.__is_mixin else data

    @classmethod
    def _make_descriptor(cls,data):
        return cls(data)
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        print(type(data))
        if data is None:
            self.__data = pd.DataFrame()
        elif type(data) is np.ndarray:
            self.__data = pd.DataFrame(data)
        
        elif type(data) is pd.core.frame.DataFrame:
            self.__data = data
            
        elif hasattr(data, '__iter__'): 
            try:
                data = pd.DataFrame(np.c_[data])
            except ValueError:
                print("[!] Cannot combine data series in the input list, shape doesn't match!")
                raise ValueError
            finally:
                self.__data = data
        elif type(data) is dict:
            data = pd.DataFrame(data)
            self.__data = data
            
        else:
            print("[!] Input data not understood !")
            print("Data should be one of the below:\n",
                  "pandas DataFrame, 2d array with time as 0th column, 1d arrray, a simple iterable")
        
            
        
    def timeSelect(self, *args):
        """
        timeSelect
        -------------
        [Input]
        :data: the time series data 2D array, with time as idx 0 column
        :args: time selection range, for time slice selection, use [t1, t2, t3]
               for multiple time range selection, use [[t1, t2], [t3, t4]]
        [Output]
        List of selected data 
        """

        for i,t in enumerate(self.timeIdx(self.__data, *args)):
            if i == 0:
                selectData = self.__data[t, :]
            else:
                selectData = np.vstack([selectData, self.__data[t, :]])
        return selectData     
    
    @staticmethod
    def cleanData(data, lowerBound = None, upperBound = None, removeOffset = True, noiseFilter = False):
        if type(data) is pd.core.DataFrame:
            data = data.values
            
        if lowerBound or upperBound:
            idxGen = TimeSeries.timeIdx(data, [lowerBound, upperBound])
            data = data[idxGen, :]
        if removeOffset:
            for i in range(1, data.shape[1]):
                offset = (np.mean(data[0:10, i]) + np.mean(data[-10:, i])) / 2
                data[:, i] = data[:, i] - offset
        return data
    
    @staticmethod
    def timeIdx(data, *args):
        
        """
        timeIdx
        -------------------
        Index a given time in the data, return closest index.
        
        [Input]
        :data: array with time as the 0th column
        :args: time values to be indexed, iterable 
               if args = t1, t2, ...., indexes for each time will be returned 
               if args = [t1, t2], [t3, t4], ... indexes for each range will be returned 
        
        [Output]
        generater of indexes corresponding to input args
        """
        if type(data) is pd.core.DataFrame:
            data = data.values
        times = data[:,0] if  len(data.shape) > 1 else data
        for t in args:            
            try:
                idx = np.argmin(abs(times - np.asarray(t))) if t else None
            except ValueError: # when t is a given range
                idx = [x if x is None else np.argmin(abs(times - x)) for x in t]
                idx0 = 0 if idx[0] is None else idx[0]
                idx1 = len(times) if idx[1] is None else idx[1]
                idx = list(range(idx0, idx1 + 1))
                pass
            finally:   
                yield idx
    
    @staticmethod
    def gaus0(x, *args):
        """
        Gaussian function with 0 offset
        """
        
        return args[0] * np.exp(- (x - args[1])**2 / (2 * args[2]**2))

    @staticmethod
    def gaus(x, *args):
        """
        Gaussian function with offset
        """
        return args[0] * np.exp(- (x - args[1])**2 / (2 * args[2]**2)) + args[3]
    
    @staticmethod
    def gausFit(x, y, plot=False):
        idxMax = np.argmax(y)
        a0 = y[idxMax]
        x0 = x[idxMax]
        halfWidth = x[idxMax + np.argmin(abs(y[idxMax:] - a0 / 2))] - x[idxMax]
        popt, pcov = curve_fit(TimeSeries.gaus0, xdata = x, ydata = y, p0 = [a0, x0, halfWidth])
        
        if plot:
            fig, ax = plt.subplots(figsize = (8,5))
            ax.plot(x, y, 'o', label = 'raw data')
            if len(x) < 10:
                xEval = np.linspace(min(x), max(x), 10 * len(x))
            else:
                xEval = x
            ax.plot(xEval, TimeSeries.gaus0(xEval, *popt), '--', label = 'gaussian fitting')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Gaussian fitting on X and Y')
            plt.show()
        else:
            pass
        popt[2] = abs(popt[2]) # sigma only takes positive value
        return (popt, pcov)
        
    def peakHeight(self, fit = False, error = False):
        if type(self.data) is pd.core.frame.DataFrame:
            data = self.data.values
            
        try:
            nRow, nCol = self.__data.shape
        except AttributeError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise AttributeError
        except ValueError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise ValueError
        else:
            if fit:
                fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
                peak, peakErr = np.array([[x[0][0], np.sqrt(x[1][0, 0])] for x in fitRes]).T
            else:
                peak = [max(k) for k in data[:, 1:].T]
        finally:            
            peak = peak[0] if len(peak) == 1 else peak               
            if fit and error:                
                peakErr = peakErr[0] if len(peakErr) == 1 else peakErr
                return(peak, peakErr)
            else:
                return(peak)
        
    def peakTime(self, fit = False, error = False):
        if type(self.data) is pd.core.frame.DataFrame:
            data = self.data.values
        try:
            nRow, nCol = data.shape
        except AttributeError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise AttributeError
        except ValueError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise ValueError
        else:
            if fit:
                fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
                peakTime, peakTimeErr = np.array([[x[0][1], np.sqrt(x[1][1, 1])] for x in fitRes]).T
            else:
                peakTime = [data[np.argmax(k), 0] for k in data[:, 1:].T]
        finally:            
            peakTime = peakTime[0] if len(peakTime) == 1 else peakTime               
            if fit and error:                
                peakTimeErr = peakTimeErr[0] if len(peakTimeErr) == 1 else peakTimeErr
                return(peakTime, peakTimeErr)
            else:
                return(peakTime)
        
    def peakFWHM(self, fit = False, error = False):
        if type(self.data) is pd.core.frame.DataFrame:
            data = self.data.values
        try:
            nRow, nCol = data.shape
        except AttributeError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise AttributeError
        except ValueError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise ValueError
        else:
            if fit:
                fitRes = [TimeSeries.gausFit(data[:,0], y) for y in data[:,1:].T]
                peakFWHM, peakFWHMErr = np.array([[x[0][2], np.sqrt(x[1][2, 2])] for x in fitRes]).T
            else:
                peakFWHM = []
                for dataY in data[:,1:].T:
                    maxIdx = np.argmax(dataY)
                    peak = dataY[maxIdx]
                    idxLow = np.argmin(np.abs(dataY[:maxIdx] - peak/2.))
                    idxHigh = np.argmin(np.abs(dataY[maxIdx:] - peak/2.)) + maxIdx
                    peakFWHM.append(data[idxHigh, 0] - data[idxLow, 0])
        finally:         
            peakFWHM = peakFWHM[0] if len(peakFWHM) == 1 else peakFWHM               
            if fit and error:                
                peakFWHMErr = peakFWHMErr[0] if len(peakFWHMErr) == 1 else peakFWHMErr
                return(peakFWHM, peakFWHM)
            else:
                return(peakFWHM)
            
    def peakIntegrate(self, fit = False, error = False):
        if type(self.data) is pd.core.frame.DataFrame:
            data = self.data.values
        try:
            nRow, nCol = data.shape
        except AttributeError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise AttributeError
        except ValueError:
            print("[!] Input data has to be 2D array with time series as 0th column!")
            raise ValueError
        else:
            if fit:
                popt = [self.gausFit(data[:,0], y)[0] for y in data[:,1:].T]
                # intergrate (-6sigma,6sigma) region 
                peakIntegrate, peakIntegrateErr = np.array([quad(TimeSeries.gaus0, y[1] - 6*y[2], y[1] + 6*y[2], args = tuple(y)) for y in popt]).T
                
            else:
                peakIntegrate = [np.trapz(x = data[:,0], y = s) for s in data[:,1:].T]
        finally:         
            peakIntegrate = peakIntegrate[0] if len(peakIntegrate) == 1 else peakIntegrate               
            if fit and error:                
                peakIntegrateErr = peakIntegrateErr[0] if len(peakIntegrateErr) == 1 else peakIntegrateErr
                return(peakIntegrate, peakIntegrate)
            else:
                return(peakIntegrate)

            
        
