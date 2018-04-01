# fullAnalysis.py --- 
# 
# Filename: fullAnalysis.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Wed Mar 28 23:05:08 2018 (-0500)
# Version: 
# Last-Updated: Sun Apr  1 17:10:42 2018 (-0500)
#           By: yulu
#     Update #: 45
# 




import numpy as np

from SciBeam.core.folderstruct import Folder
from SciBeam.core.io import Loader
from SciBeam.core.timeseries import TimeSeries

class Analysis(Folder, Loader, TimeSeries):

    def __init__(self, path):
        Folder.__init__(self, path)
        Loader.__init__(self, None)
        TimeSeries.__init__(self, None)
    
        
        #LoadDictFile.__init__(fileDict)
        

    
