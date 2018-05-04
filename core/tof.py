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
# Last-Updated: Fri May  4 12:27:07 2018 (-0500)
#           By: yulu
#     Update #: 22
# 


import numpy as np
import os
import re

from SciBeam.core.common import (
    winPathHandler,
    loadFile,
    )


class TOF:
    """
    Single time-of-flight data analysis
    """

    def __init__(self, path):
        self.path = path
        self.data = self.load()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = winPathHandler(path)

    def load(self):
        return loadFile(self.path)

    @property
    def shape(self):
        return self.data.shape

    @property
    def info(self):
        delta_t = np.unique(self.data[1:, 0] - self.data[:-1, 0])
        max_value = max(self.data[:,1])
        min_value = min(self.data[:,1])
        start_t = min(self.data[:,0])
        end_t = max(self.data[:,0])

        print('SciBeam.TOF.info:')
        print('--------------------')
        print('Start time: %f' %start_t)
        print('End time: %f' %end_t)
        print('Max value: %f' %max_value)
        print('Min value: %f' %min_value)
        print('--------------------')
    

    
        
    
