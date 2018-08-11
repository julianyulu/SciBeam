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
# Last-Updated: Tue Jul 24 23:55:25 2018 (-0500)
#           By: yulu
#     Update #: 315
# 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scibeam.core.formatter import format_dict
from scibeam.core import base
from scibeam.core.gaussian import Gaussian
from scibeam.core import numerical

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
    
    def image(self, sideplots = True, add_contour = False, **kwargs):
        """
        image plot of tof data measured multiplot positions
        """
        
        if 'figsize' in kwargs:
            plt.figure(figsize = kwargs.pop('figsize'))
        else:
            plt.figure(figsize = (6,6))
        
        if sideplots:
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
        else:
            im = plt.imshow(np.flipud(self.data.values.T), 
                            **kwargs,
                            aspect = 'auto',
                            extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],

                            )
            plt.xlabel(self.index_label if self.index_label else 'Time of flight')
            plt.ylabel(self.column_label if self.column_label else 'Position')
            cbar = plt.colorbar(im)
            #cbar.ax.set_ylabel('Signal')
            
        if add_contour:
            if sideplots:
                self.contour(colors = 'w', ax = axImg, title = '', xlabel = '', ylabel = '')
            else:
                self.contour(colors = 'w', title = '', xlabel = '', ylabel = '')
               
        
    def contour(self, n_contours = 5, n_sigma = 2, xlabel = 'time', ylabel = 'value', title = 'contour plot', label = None,
           ax = None, **kwargs):
        """
        contour plots for 2D self.data

        """
        popt = self.data.peak.height().gausFit()[0]
        n_sigma_levels = Gaussian.gaus(popt[1] + np.linspace(n_sigma, 0.2 ,  n_contours)* popt[2], *popt)
        if ax:
            ax.contour(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            
        else:
            plt.contour(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
   
    def contourf(self, n_contours = 5, n_sigma = 2, xlabel = 'time', ylabel = 'value', title = 'contour plot', label = None,
           ax = None, **kwargs):
        """
        contourf plots for 2D self.data

        """
        popt = self.data.peak.height().gausFit()[0]
        n_sigma_levels = Gaussian.gaus(popt[1] + np.linspace(n_sigma, 0.2 ,  n_contours)* popt[2], *popt)
        if ax:
            ax.contourf(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        else:
            plt.contourf(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)



