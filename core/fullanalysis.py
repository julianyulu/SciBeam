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
# Last-Updated: Thu Mar 29 21:01:33 2018 (-0500)
#           By: yulu
#     Update #: 35
# 

import numpy as np

from SciBeam.core.folderstruct import Folder
from SciBeam.core.dataio import LoadDictFile
from SciBeam.core.timeseries import TimeSeries

class Analysis(Folder, LoadDictFile):#, TimeSeries):
    
    
    def __init__(self, path, fileDict = None, ):
        Folder.__init__(self, path)
        
        #LoadDictFile.__init__(fileDict)
        

    
