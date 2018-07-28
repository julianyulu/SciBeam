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
# Last-Updated: Sat Jul 28 15:04:02 2018 (-0500)
#           By: yulu
#     Update #: 59
# 

import unittest
import pkg_resources
import re
from scibeam import RegMatch



DATA_PATH = pkg_resources.resource_filename('scibeam', 'data/test/time_series_2D/')

class TestRegmatch(unittest.TestCase):
    def setUp(self):
        try:
            self.rgm_single = RegMatch('.*_(\d+\.\d+)in_.*.lvm$')
            self.rgm_multi = RegMatch(['.*_(APD\d+)_.*.lvm$', '.*_(\d+\.\d+)in_.*.lvm$'])
        except:
            self.fail("Initialize class RegMatch instance failed !")
        else:
            self.assertTrue(hasattr(self.rgm_single.regex, 'match'))
            self.assertTrue(hasattr(self.rgm_multi.regex, '__iter__'))
            
    def test_single_regex_match(self):
        sample = ['20180314_APD1_0.77500in_scan.lvm', '20180314_APD1_0.92500in_scan.lvm']
        regex = '.*(APD\d+)_(\d+\.\d+)in_.*.lvm$'

        # Test when being matched is a single string 
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 1, asNumber = False),
                         {'APD1': '20180314_APD1_0.77500in_scan.lvm'})
        
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 2, asNumber = False),
                         {'0.77500': '20180314_APD1_0.77500in_scan.lvm'})
        
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample[0], group = 2, asNumber = True),
                         {0.775: '20180314_APD1_0.77500in_scan.lvm'})

        # Test when being matched is a list of strings
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 1, asNumber = False),
                         {'APD1': ['20180314_APD1_0.77500in_scan.lvm', '20180314_APD1_0.92500in_scan.lvm']})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 2, asNumber = False),
                         {'0.77500': '20180314_APD1_0.77500in_scan.lvm', '0.92500':  '20180314_APD1_0.92500in_scan.lvm'})
        self.assertEqual(self.rgm_single.single_regex_match(regex, sample, group = 2, asNumber = True),
                         {0.775: '20180314_APD1_0.77500in_scan.lvm', 0.925: '20180314_APD1_0.92500in_scan.lvm'})

        
    def test_match(self):
        sample = ['20180314_APD1_0.77500in_scan.lvm', '20180314_APD1_0.92500in_scan.lvm']

        # one to one
        self.assertEqual(self.rgm_single.match(sample[0], group = 1, asNumber = True),
                         {0.775: '20180314_APD1_0.77500in_scan.lvm'})
        self.assertEqual(self.rgm_single.match(sample[0], group = 1, asNumber = False),
                         {'0.77500': '20180314_APD1_0.77500in_scan.lvm'})

        # one to multi 
        self.assertEqual(self.rgm_single.match(sample, group = 1, asNumber = True),
                         {0.775: '20180314_APD1_0.77500in_scan.lvm',
                          0.925: '20180314_APD1_0.92500in_scan.lvm'})
        self.assertEqual(self.rgm_single.match(sample, group = 1, asNumber = False),
                         {'0.77500': '20180314_APD1_0.77500in_scan.lvm',
                          '0.92500': '20180314_APD1_0.92500in_scan.lvm'})

        # multi to one
        self.assertEqual(self.rgm_multi.match(sample[0], group = 1, asNumber = False),
                         [{'APD1': '20180314_APD1_0.77500in_scan.lvm'},
                          {'0.77500': '20180314_APD1_0.77500in_scan.lvm'}])

        # multi to multi
        self.assertEqual(self.rgm_multi.match(sample, group = 1, asNumber = False),
                         [{'APD1': ['20180314_APD1_0.77500in_scan.lvm',
                                    '20180314_APD1_0.92500in_scan.lvm']},
                          {'0.77500': '20180314_APD1_0.77500in_scan.lvm',
                           '0.92500': '20180314_APD1_0.92500in_scan.lvm'}])


    def test_matchFolder(self):
        self.assertEqual(self.rgm_single.matchFolder(DATA_PATH, asNumber = True),
        {0.3: '20180314_APD1_0.30000in_scan.lvm',
         0.325: '20180314_APD1_0.32500in_scan.lvm',
         0.35: '20180314_APD1_0.35000in_scan.lvm',
         0.375: '20180314_APD1_0.37500in_scan.lvm',
         0.4: '20180314_APD1_0.40000in_scan.lvm'})

        self.assertEqual(self.rgm_single.matchFolder(DATA_PATH, asNumber = False),
        {'0.30000': '20180314_APD1_0.30000in_scan.lvm',
         '0.32500': '20180314_APD1_0.32500in_scan.lvm',
         '0.35000': '20180314_APD1_0.35000in_scan.lvm',
         '0.37500': '20180314_APD1_0.37500in_scan.lvm',
         '0.40000': '20180314_APD1_0.40000in_scan.lvm'})


        self.assertEqual(self.rgm_multi.matchFolder(DATA_PATH, asNumber = False),
        {'APD1':
         {'0.30000': '20180314_APD1_0.30000in_scan.lvm',
         '0.32500': '20180314_APD1_0.32500in_scan.lvm',
         '0.35000': '20180314_APD1_0.35000in_scan.lvm',
         '0.37500': '20180314_APD1_0.37500in_scan.lvm',
         '0.40000': '20180314_APD1_0.40000in_scan.lvm'}
        })
        
        
