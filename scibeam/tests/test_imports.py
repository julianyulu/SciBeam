# test_import.py --- 
# 
# Filename: test_import.py
# Description: 
#            unittests for __init__ import  
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat Jul 21 07:07:02 2018 (-0500)
# Version: 
# Last-Updated: Tue Jul 24 23:52:33 2018 (-0500)
#           By: yulu
#     Update #: 17
# 

import unittest
import scibeam

class TestImports(unittest.TestCase):
    
            
    def test_import_TOFFrame(self):
        self.assertEqual(scibeam.TOFFrame, scibeam.core.tofframe.TOFFrame)

    def test_import_TOFSeries(self):
        self.assertEqual(scibeam.TOFSeries, scibeam.core.tofseries.TOFSeries)
        
    def test_import_read_folder(self):
        self.assertEqual(scibeam.read_folder, scibeam.core.tofframe.read_folder)

    def test_import_read_file(self):
        self.assertEqual(scibeam.read_file, scibeam.core.tofseries.read_file)

    def test_import_RegMatch(self):
        self.assertEqual(scibeam.RegMatch, scibeam.core.regexp.RegMatch)

    def test_import_PlotTOFSeries(self):
        self.assertEqual(scibeam.PlotTOFSeries, scibeam.core.plot.PlotTOFSeries)

    def test_import_Gaussian(self):
        self.assertEqual(scibeam.Gaussian, scibeam.core.gaussian.Gaussian)
    

if __name__ == '__main__':
    unittest.main()
