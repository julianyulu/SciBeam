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
# Last-Updated: Tue Jul 24 23:49:48 2018 (-0500)
#           By: yulu
#     Update #: 45
#

import unittest
from scibeam.core.base import _is_mixin, _mixin_class
from scibeam import TOFFrame, TOFSeries, Gaussian

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
