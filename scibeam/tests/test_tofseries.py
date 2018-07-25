# test_tofseries.py --- 
# 
# Filename: test_tofseries.py
# Description: 
#            unittests of tofseries
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat Jul 21 07:25:44 2018 (-0500)
# Version: 
# Last-Updated: Wed Jul 25 00:20:17 2018 (-0500)
#           By: yulu
#     Update #: 29
# 

import unittest
from scibeam import TOFSeries, read_file
import pkg_resources

DATA_FILE = pkg_resources.resource_filename('scibeam', 'examples/data/time_series_1D/single_time_series.lvm')


class TestFunctions(unittest.TestCase):
    
    def test_read_defaults(self):
        try:
            ds = read_file(DATA_FILE)
        except:
            self.fail("File read-in failed !")
        else:
            self.assertEqual(ds.shape, (25000, ))
            self.assertTrue(isinstance(ds, TOFSeries))
        
    def test_read_with_bounds(self):
        try:
            ds = read_file(DATA_FILE, lowerBound = 500e-6, upperBound = 600e-6)
        except:
            self.fail("File read-in failed !")
        self.assertTrue(abs(ds.index[0] - 500e-6) < 1e-6)
        self.assertTrue(abs(ds.index[-1] - 600e-6) < 1e-6)

    def test_read_without_offset(self):
        try:
            ds = read_file(DATA_FILE, lowerBound = 500e-6, upperBound = 600e-6, removeOffset = False)
            ds2 = read_file(DATA_FILE, lowerBound = 500e-6, upperBound = 600e-6, removeOffset = True)
        except:
            self.fail("File read-in failed !")
        self.assertTrue(abs(ds - ds2).sum() > 0.01)

        
#class TestTOFSeries(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
