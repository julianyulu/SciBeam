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
# Last-Updated: Sat Jul 21 07:36:58 2018 (-0500)
#           By: yulu
#     Update #: 15
# 

import unittest
import SciBeam

class TestImports(unittest.TestCase):
    
            
    def test_import_TOFFrame(self):
        self.assertEqual(SciBeam.TOFFrame, SciBeam.core.tofframe.TOFFrame)

    def test_import_TOFSeries(self):
        self.assertEqual(SciBeam.TOFSeries, SciBeam.core.tofseries.TOFSeries)
        
    def test_import_read_folder(self):
        self.assertEqual(SciBeam.read_folder, SciBeam.core.tofframe.read_folder)

    def test_import_read_file(self):
        self.assertEqual(SciBeam.read_file, SciBeam.core.tofseries.read_file)

    def test_import_RegMatch(self):
        self.assertEqual(SciBeam.RegMatch, SciBeam.core.regexp.RegMatch)

    def test_import_PlotTOFSeries(self):
        self.assertEqual(SciBeam.PlotTOFSeries, SciBeam.core.plot.PlotTOFSeries)

    def test_import_Gaussian(self):
        self.assertEqual(SciBeam.Gaussian, SciBeam.core.gaussian.Gaussian)
    

if __name__ == '__main__':
    unittest.main()
