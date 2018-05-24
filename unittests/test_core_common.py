# test_core_common.py --- 
# 
# Filename: test_core_common.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri May  4 11:33:37 2018 (-0500)
# Version: 
# Last-Updated: Wed May 23 20:10:41 2018 (-0500)
#           By: yulu
#     Update #: 10
# 

import unittest
import os
import numpy as np 
#test_data_root = '../examples/data/'

from SciBeam.core.common  import Common
    


class TestFunctions(unittest.TestCase):
    '''
    Test core.common.py
    '''

    def test_winPathHandler(self):
        test_path_win = r'C:\Documents\MyFolder\Whatever.txt'
        test_path_linux = '/home/MyFolder/Whatever.txt'

        self.assertEqual(Common.winPathHandler(test_path_win), 'C:/Documents/MyFolder/Whatever.txt')
        self.assertEqual(Common.winPathHandler(test_path_linux), '/home/MyFolder/Whatever.txt')
        self.assertEqual(Common.winPathHandler([test_path_win, test_path_linux]),['C:/Documents/MyFolder/Whatever.txt','/home/MyFolder/Whatever.txt'])
    


    def test_loadFile(self):
        testFile = '../examples/data/time_series_1D/single_time_series.lvm'
        self.assertEqual(Common.loadFile(testFile).shape, (25000, 2))
        
if __name__ == '__main__':
    unittest.main()

        
