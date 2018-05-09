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
# Last-Updated: Tue May  8 23:17:22 2018 (-0500)
#           By: yulu
#     Update #: 61
# 

import numpy as np
import matplotlib.pyplot as plt
from SciBeam.core import base

class Plot:
    def __init__(self, dataframe):
        self.__is_mixin = base._is_mixin(dataframe)
        self.data = dataframe._make_mixin if self.__is_mixin else dataframe

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

    def scanPlot(self, **kwargs):
        figureKwds = ['figsize', 'ncols', 'nrows','sharex', 'sharey']

        figure_setup = {y[0]: y[1] for y in  [(x, kwargs.pop(x)) for x in figureKwds if x in kwargs]}
        
        fig, ax = plt.subplots(**figure_setup)

        
        #if len(ax) == 1:
            #ax.plot(df.index, df[0.3])
        #else:
         #   ax[i].plot(df
        
        
            
