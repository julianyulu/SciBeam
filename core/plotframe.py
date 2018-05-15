# plotframe.py --- 
# 
# Filename: plotframe.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun May  6 16:47:06 2018 (-0500)
# Version: 
# Last-Updated: Tue May 15 00:21:41 2018 (-0500)
#           By: yulu
#     Update #: 212
# 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from SciBeam.core import base
from SciBeam.core import numerical

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
            fig = plt.figure(figsize = kwargs.pop('figsize'))
        else:
            pass
            fig = plt.figure(figsize = (6,6))

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
        

        axImg = fig.add_axes(rect_img)
        axDistrx = fig.add_axes(rect_distx)
        axDistry = fig.add_axes(rect_disty)
        cax = fig.add_axes(rect_cax)
        # no labels
        axDistrx.xaxis.set_major_formatter(nullfmt)
        axDistry.yaxis.set_major_formatter(nullfmt)


        areaDataY = [np.trapz(x = self.data.index, y = self.data[x]) for x in self.data]
        areaDataX = [np.trapz(x = self.data.columns, y = self.data.loc[x,:]) for x in self.data.index]
        axDistrx.plot(self.data.index, areaDataX)
        axDistry.plot(areaDataY, self.data.columns)
        axDistry.invert_yaxis()
        
        
        im = axImg.imshow(self.data.T,
                        **kwargs,
                        aspect = 'auto',
                        extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],
                        
                        )
        
        
        axImg.set_xlabel(self.index_label if self.index_label else 'Time of flight')
        axImg.set_ylabel(self.column_label if self.column_label else 'Position')
        cbar = fig.colorbar(im,  cax = cax)
        #cbar.ax.set_ylabel('Signal')
        
        return fig, (axImg, axDistrx, axDistry)

