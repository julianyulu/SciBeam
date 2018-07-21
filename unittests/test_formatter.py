# test_formatter.py --- 
# 
# Filename: test_formatter.py
# Description: 
#            Unittests for formatter functions 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Thu Jul 19 11:26:04 2018 (-0500)
# Version: 
# Last-Updated: Fri Jul 20 23:54:53 2018 (-0500)
#           By: yulu
#     Update #: 12
# 

import unittest
from SciBeam.core.formatter import format_dict

class TestFunctions(unittest.TestCase):
    testDict = {'d': 4,
                'c': 3.1415926,
                'e': 5,
                'b': 2,
                'a': 1
                }

    def test_formart_dict(self):
        self.assertEqual(format_dict(self.testDict, alphabetical = False, digits = 2),
                         'd: 4.00\nc: 3.14\ne: 5.00\nb: 2.00\na: 1.00')

        self.assertEqual(format_dict(self.testDict, alphabetical = True, digits = 2),
                         'a: 1.00\nb: 2.00\nc: 3.14\nd: 4.00\ne: 5.00')
        self.assertEqual(format_dict(self.testDict, alphabetical = True, digits = 5),
                         'a: 1.00000\nb: 2.00000\nc: 3.14159\nd: 4.00000\ne: 5.00000')


if __name__ == '__main__':
    unittest.main()
                         
