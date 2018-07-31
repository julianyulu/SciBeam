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
# Last-Updated: Mon Jul 30 22:34:52 2018 (-0500)
#           By: yulu
#     Update #: 60
# 

import unittest
import pkg_resources
import numpy as np 
from scibeam import TOFSeries, read_file


DATA_FILE = pkg_resources.resource_filename('scibeam', 'data/test/time_series_1D/single_time_series.lvm')


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
        ds = read_file(DATA_FILE, lowerBound = 500e-6, upperBound = 600e-6)
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

        
class TestTOFSeries(unittest.TestCase):

    def setUp(self):
        try:
            self.series = TOFSeries.from_file(DATA_FILE)
        except:
            self.fail("TOFSeries initialize failed !")

    def test_init(self):
        self.assertTrue(hasattr(self.series, 'head'))

    def test_find_time_idx(self):
        self.assertEqual(list(self.series.find_time_idx(self.series.index, 1000e-6)), [2500])
        self.assertEqual(list(self.series.find_time_idx(self.series.index, 1000e-6, 1100e-6, 1200e-6)), [2500, 2750, 3000])
        self.assertEqual(list(self.series.find_time_idx(self.series.index, [1000e-6, 1100e-6, 1200e-6])), [2500, 2750, 3000])

    def test_remove_data_offset(self):
        sample_data = np.ones(1000)
        sample_data[450:550] = 10
        sample_data_offset_removed1 = TOFSeries.remove_data_offset(sample_data,
                                                                  lowerBoundIdx = 400,
                                                                  upperBoundIdx = 600)
        sample_data_offset_removed2 = TOFSeries.remove_data_offset(sample_data)
        
        self.assertTrue((sample_data_offset_removed1[450:550] == 9).any())
        self.assertTrue((sample_data_offset_removed1[:200] == 0).any())
        self.assertTrue((sample_data_offset_removed2[450:550] == 9).any())
        self.assertTrue((sample_data_offset_removed2[:200] == 0).any())

    

        

    
        
        

if __name__ == '__main__':
    unittest.main()
