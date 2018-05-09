# plot.py --- 
# 
# Filename: plot.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun May  6 16:47:06 2018 (-0500)
# Version: 
# Last-Updated: Wed May  9 00:52:27 2018 (-0500)
#           By: yulu
#     Update #: 96
# 

import numpy as np
import matplotlib.pyplot as plt
from SciBeam.core import base
from SciBeam.core import numerical

class Plot:
    """
    Plot dataframe with time as index and another numerical variable as 
    column labels 
    """
    def __init__(self, dataframe):
        self.__is_mixin = base._is_mixin(dataframe)
        self.data = dataframe._make_mixin if self.__is_mixin else dataframe
        self.position = np.array(self.data.columns)
        self.time = np.array(self.data.index)
        

    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, dataframe):
        self.__data = dataframe

    @classmethod
    def _make_descriptor(cls, data):
        return cls(data)
    
    def image(self, **kwargs):
        """
        image plot of tof data measured multiplot positions
        """
        
        if 'figsize' in kwargs:
            fig, ax = plt.subplots(figsize = kwargs.pop('figsize'))
        else:
            fig, ax = plt.subplots()
            
        cax = ax.imshow(self.data.T,
                        **kwargs,
                        aspect = 'auto',
                        extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],
                        
                        )

        ax.set_xlabel('Time of flight [us]')
        ax.set_ylabel('Position')
        cbar = fig.colorbar(cax)
        cbar.set_label('Signal')
        return fig, ax

    def peakPlot(self, fit_tof = False, fit_result = True, print_fit_params = True, **kwargs):
        """
        Plot peak height for each columns in dataframe
        """

        if fit_tof:
            popt_pcov_series = self.data.apply(lambda s: numerical.gausFit(y = s.values, x = s.index))
            peaks = [popt_pcov_series.values[i][0][0] for i in range(len(popt_pcov_series))]
            
            
        else:
            peaks = self.data.max().values
            
        if 'figsize' in kwargs:
            fig, ax = plt.subplots(figsize = kwargs.pop('figsize'))
        else:
            fig, ax = plt.subplots()


        ax.plot(self.position, peaks, 'o', label = 'peak')

        if fit_result:
            popt, pcov = numerical.gausFit(x = self.position, y = peaks)
            fitX = np.linspace(min(self.position), max(self.position), 100)
            ax.plot(fitX, numerical.gaus(fitX, *popt), 'r-', label = "Gaussian Fit")
            ax.legend()

        if fit_result and print_fit_params:
            print("===============================")
            print("Gaussian fit parameters:",
                  "\nHeight: {:.3f}\nCenter: {:.3f}\nSigma: {:.3f}\nFWHM: {:.3f}".format(
                      popt[0],
                      popt[1],
                      popt[2],
                      2.355 * popt[2],
                      ))
            print("===============================")
            
        return fig, ax
        
        

    # def scanPlot(self, **kwargs):
    #     figureKwds = ['figsize', 'ncols', 'nrows','sharex', 'sharey']

    #     figure_setup = {y[0]: y[1] for y in  [(x, kwargs.pop(x)) for x in figureKwds if x in kwargs]}
        
    #     fig, ax = plt.subplots(**figure_setup)

        
    #     #if len(ax) == 1:
    #         #ax.plot(df.index, df[0.3])
    #     #else:
    #      #   ax[i].plot(df
        
        
            
