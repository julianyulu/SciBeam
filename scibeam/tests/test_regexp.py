# test_regexp.py --- 
# 
# Filename: test_regexp.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Wed Jul 25 00:17:55 2018 (-0500)
# Version: 
# Last-Updated: Wed Jul 25 00:53:39 2018 (-0500)
#           By: yulu
#     Update #: 23
# 

import unittest
import pkg_resources
import re
from scibeam import RegMatch



DATA_FILE = pkg_resources.resource_filename('scibeam', 'examples/data/time_series_2D/')

class TestRegmatch(unittest.TestCase):
    def setUp(self):
        try:
            self.rgm_single = RegMatch('.*_(\d+\.\d+)in_.*.lvm$')
            self.rgm_multi = RegMatch(['.*_(0.6\d+)in_.*.lvm$', '.*_(\d+\.\d+)in_.*.lvm$'])
        except:
            self.fail("Initialize class RegMatch instance failed !")
        else:
            self.assertTrue(hasattr(self.rgm_single.regex, 'match'))
            self.assertTrue(hasattr(self.rgm_multi.regex, '__iter__'))
            
    def test_single_regex_match(self):
        sample = ['20180314_APD1_0.77500in_scan.lvm', '20180314_APD1_0.92500in_scan.lvm']
        regex = '.*(APD\d+)_(\d+\.\d+)in_.*.lvm$'

        # Test when being matched is a single string 
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 1, asNumber = False), {'APD1': '20180314_APD1_0.77500in_scan.lvm'})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 2, asNumber = False), {'0.77500': '20180314_APD1_0.77500in_scan.lvm'})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 2, asNumber = True), {0.775: '20180314_APD1_0.77500in_scan.lvm'})

        # Test when being matched is a list of strings
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 1, asNumber = False), {'APD1': ['20180314_APD1_0.77500in_scan.lvm', '20180314_APD1_0.92500in_scan.lvm']})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 2, asNumber = False), {'0.77500': '20180314_APD1_0.77500in_scan.lvm', '0.92500':  '20180314_APD1_0.92500in_scan.lvm'})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 2, asNumber = True), {0.775: '20180314_APD1_0.77500in_scan.lvm', 0.925: '20180314_APD1_0.92500in_scan.lvm'})

        
        
       
        
    

