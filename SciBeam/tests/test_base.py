# test_base.py --- 
# 
# Filename: test_base.py
# Description:
#           Unit test case for base.py
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Thu Mar 29 10:44:57 2018 (-0500)
# Version: 
# Last-Updated: Thu Jul 19 11:47:59 2018 (-0500)
#           By: yulu
#     Update #: 44
# 

import unittest
from SciBeam.core.base import _is_mixin, _mixin_class
from SciBeam import TOFFrame, TOFSeries, Gaussian

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.tofseries = TOFSeries()
        self.tofframe = TOFFrame()
        self.gaussian = Gaussian
        
    def test_is_mixin(self):
        self.assertTrue(_is_mixin(self.tofseries))
        self.assertTrue(_is_mixin(self.tofframe))
        self.assertFalse(_is_mixin(self.gaussian))
        
if __name__ == '__main__':
    unittest.main()
