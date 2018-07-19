# plotseries.py --- 
# 
# Filename: plotseries.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun May  6 16:47:06 2018 (-0500)
# Version: 
# Last-Updated: Thu Jul 19 10:57:38 2018 (-0500)
#           By: yulu
#     Update #: 314
# 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from SciBeam.core.formatter import format_dict
from SciBeam.core import base
from SciBeam.core.gaussian import Gaussian
from SciBeam.core import numerical

class PlotTOFSeries:
    """
    Plot dataframe with time as index and another numerical variable as 
    column labels 
    """
    def __init__(self, dataseries, lowerBound = None, upperBound = None, index_label = None, column_name = None):
        self.__is_mixin = base._is_mixin(dataseries)
        self.data = dataseries._make_mixin if self.__is_mixin else dataseries
        self.index_label = index_label
        self.column_name = column_name

    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, dataseries):
        self.__data = dataseries

    @classmethod
    def _constructor(cls, data):
        return cls(data)


    def plot(self, ax = None, gauss_fit = True, gauss_fit_offset = 0, print_fit_params = True, title = None, xlabel = None, ylabel = None, label = None, params_digits = 3, **kwargs):

        
        if ax is None:
            plt.plot(self.data.index, self.data.values, 'o', **kwargs)
                        
            if gauss_fit:
                popt, pcov = Gaussian.gausFit(x = self.data.index, y = self.data.values, offset = gauss_fit_offset)
                fit_params = {'a': popt[0], 'x0': popt[1], '$\sigma$': popt[2]}
                smoothX = np.linspace(popt[1] - 3* popt[2], popt[1] + 3 * popt[2], 5 * len(self.data.index))
                plt.plot(smoothX, Gaussian.gaus(smoothX, *popt), 'r-')
                plt.figtext(0.95, 0.85, 'fitting parameters:\n' + format_dict(fit_params, digits = params_digits), verticalalignment='top', horizontalalignment='left')
                
                plt.legend(['data', 'gauss fit'])
            else:
                pass

            # if no gauss_fit, the 2nd label will be muted
            if label: plt.legend([label, 'gauss fit'])
            if ylabel: plt.ylabel(ylabel)
            if xlabel: plt.xlabel(xlabel)
            if title: plt.title(title)
            
        else:
            ax.plot(self.data.index, self.data.values, 'o', **kwargs)
            if gauss_fit:
                popt, pcov = Gaussian.gausFit(x = self.data.index, y = self.data.values , offset = gauss_fit_offset)
                smoothX = np.linspace(popt[1] - 3* popt[2], popt[1] + 3 * popt[2], 5 * len(self.data.index))
                ax.plot(smoothX, Gaussian.gaus(smoothX, *popt), 'r-', **kwargs)
                ax.legend(['data', 'gauss fit'])
                fit_params = {'a': popt[0], 'x0': popt[1], '$\sigma$': popt[2]}
                plt.figtext(0.95, 0.85, 'fitting parameters:\n' + format_dict(fit_params, digits = params_digits), verticalalignment='top', horizontalalignment='left')
            else:
                pass

            # if no gauss_fit, the 2nd label will be muted, otherwise will overwrite
            if label: ax.legend([label, 'gauss fit'])
            if ylabel: ax.set_ylabel(ylabel)
            if xlabel: ax.set_xlabel(xlabel)
            if title: ax.set_title(title)




class PlotTOFFrame:
    """
    Plot dataframe with time as index and another numerical variable as 
    column labels 
    """
    def __init__(self, dataframe, lowerBound = None, upperBound = None, index_label = None, column_label = None):
        self.__is_mixin = base._is_mixin(dataframe)
        self.data = dataframe._make_mixin if self.__is_mixin else dataframe
        self.index_label = index_label
        self.column_label = column_label
    
    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, dataframe):
        self.__data = dataframe

    @classmethod
    def _constructor(cls, data):
        return cls(data)
    
    def image(self, **kwargs):
        """
        image plot of tof data measured multiplot positions
        """
        
        if 'figsize' in kwargs:
            plt.figure(figsize = kwargs.pop('figsize'))
        else:
            plt.figure(figsize = (6,6))

        nullfmt = NullFormatter()         # no labels

        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        bottom_h = left_h = left + width + 0.02

        rect_img = [left, bottom, width, height]
        rect_distx = [left, bottom_h, width, 0.2]
        rect_disty = [left_h, bottom, 0.2, height]
        rect_cax = [left_h, bottom_h, 0.1, 0.2]

        # start with a rectangular Figure
        axImg = plt.axes(rect_img)
        axDistrx = plt.axes(rect_distx)
        axDistry = plt.axes(rect_disty)
        cax = plt.axes(rect_cax)
        # no labels
        axDistrx.xaxis.set_major_formatter(nullfmt)
        axDistry.yaxis.set_major_formatter(nullfmt)


        areaDataY = [np.trapz(x = self.data.index, y = self.data[x]) for x in self.data]
        areaDataX = [np.trapz(x = self.data.columns, y = self.data.loc[x,:]) for x in self.data.index]
        axDistrx.plot(self.data.index, areaDataX)
        axDistry.plot(areaDataY, self.data.columns)
        #axDistry.invert_yaxis() # don't need to invert anymore 
        
        # has to flip data so that lower position starts from lower part of the image 
        im = axImg.imshow(np.flipud(self.data.values.T), 
                        **kwargs,
                        aspect = 'auto',
                        extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],
                        
                        )
        
        
        axImg.set_xlabel(self.index_label if self.index_label else 'Time of flight')
        axImg.set_ylabel(self.column_label if self.column_label else 'Position')
        cbar = plt.colorbar(im,  cax = cax)
        #cbar.ax.set_ylabel('Signal')


