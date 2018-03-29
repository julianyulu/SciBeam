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
# Last-Updated: Thu Mar 29 01:33:42 2018 (-0500)
#           By: yulu
#     Update #: 20
# 

import numpy as np

from SciBeam.core.folderstruct import Folder
from SciBeam.core.dataio import LoadDictFile
from SciBeam.core.timeseries import TimeSeries

class Analysis:
    
    
    def __init__(self, path):
        self.path = path
        self.Folder = Folder(path)
        self.LoadDictFile = LoadDictFile.__init__(self.Folder, self.Folder.query_result)

    def myloadfile(self):
        return LoadDictFile(self.Folder.query_result)
        

    
