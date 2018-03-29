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
# Last-Updated: Thu Mar 29 11:41:54 2018 (-0500)
#           By: yulu
#     Update #: 9
# 

import unittest
import os
import numpy as np 
#test_data_root = '../examples/data/'

from SciBeam.core import base

class TestFunctions(unittest.TestCase):
    def test_buildDict(self):
        emptyDict = {}
        popedDict = {'a': 1}
        # insert to empty dict
        testDict1 = base.buildDict(empty, 'a', 1)
        self.assertEqual(testDict1['1'], 2)
        self.assertEqual(emptyDict['1'], 2)

        # insert to populated dict
        testDict2 = base.buildDict(popedDict, 'b', 2)
        self.assertEqual(testDict2['b'], 2)
        self.assertEqual(testDict2['a'], 1)
        self.assertEqual(popedDict2['b'], 2)
        self.assertEqual(popedDict2['a'], 1)

        # insert with repeated key
        testDict3 = base.buildDict(popedDict, 'a', 3)
        self.assertEqual(testDict3['a'], [1,3])
        self.assertEqual(testDict3['b'], 2)
        self.assertEqual(popedDict3['a'], [1,3])
        self.assertEqual(popedDict3['b'], 2)


    def test_pathJoin(self):
        test_path_win = r'C:\Documents\MyFolder\Whatever'
        test_path_linux1 = '/home/MyFolder/Whatever'
        test_path_linux2 = '/home/MyFolder/Whatever/'

        test_target1 = 'folder1'
        test_target2 = '/folder2'
        test_target3 = 'folder3/'
        test_target4 = '/folder4/'

        #test windows raw path
        self.assertEqual(base.pathJoin(test_path_win, test_target1), 'C:/Documents/MyFolder/Whatever/folder1/')
        self.assertEqual(base.pathJoin(test_path_win, test_target2), 'C:/Documents/MyFolder/Whatever/folder2/')
        self.assertEqual(base.pathJoin(test_path_win, test_target3), 'C:/Documents/MyFolder/Whatever/folder3/')
        self.assertEqual(base.pathJoin(test_path_win, test_target4), 'C:/Documents/MyFolder/Whatever/folder4/')
        self.assertEqual(base.pathJoin(test_path_win, test_target1, test_target2, test_target3, test_target4), 'C:/Documents/MyFolder/Whatever/folder1/folder2/folder3/folder4/')

        # test linux path
        self.assertEqual(base.pathJoin(test_path_linux1, test_target1), '/home/MyFolder/Whatever/folder1/')
        self.assertEqual(base.pathJoin(test_path_linux1, test_target2), '/home/MyFolder/Whatever/folder2/')
        self.assertEqual(base.pathJoin(test_path_linux1, test_target3), '/home/MyFolder/Whatever/folder3/')
        self.assertEqual(base.pathJoin(test_path_linux1, test_target4), '/home/MyFolder/Whatever/folder4/')
        self.assertEqual(base.pathJoin(test_path_linux1, test_target1, test_target2, test_target3, test_target4), '/home/MyFolder/Whatever/folder1/folder2/folder3/folder4/')
        self.assertEqual(base.pathJoin(test_path_linux2, test_target1), '/home/MyFolder/Whatever/folder1/')
        self.assertEqual(base.pathJoin(test_path_linux2, test_target2), '/home/MyFolder/Whatever/folder2/')
        self.assertEqual(base.pathJoin(test_path_linux2, test_target3), '/home/MyFolder/Whatever/folder3/')
        self.assertEqual(base.pathJoin(test_path_linux2, test_target4), '/home/MyFolder/Whatever/folder4/')
        self.assertEqual(base.pathJoin(test_path_linux2, test_target1, test_target2, test_target3, test_target4), '/home/MyFolder/Whatever/folder1/folder2/folder3/folder4/')
        

