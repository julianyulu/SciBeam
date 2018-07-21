# regexp.py --- 
# 
# Filename: regexp.py
# Description: 
#            Python regex related functions 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat May  5 16:24:14 2018 (-0500)
# Version: 
# Last-Updated: Mon Jul  9 11:03:46 2018 (-0500)
#           By: yulu
#     Update #: 213
# 

from SciBeam.core.common import winPathHandler
from SciBeam.util.dictfunc import buildDict
from SciBeam.core import base
import os, re

class RegMatch:
    def __init__(self, regStr):
        self.regex = regStr

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, regStr):
        if type(regStr) == list:
            self._regex =  [re.compile(s) for s in regStr]
        else:
            self._regex = re.compile(regStr)

    
    @staticmethod
    def single_regex_match(regStr, strings, group = 1, asNumber = False):
        """
        Match python regex pattern in a given string or list of strings
        Based on python re package and uses group to locate the value 

        returns pairs of (value, string) matched pairs
        """
        
        if type(strings) == list: # for list of strings to be matched 
            matched = []
            for oneStr in strings:
                mch = regStr.match(oneStr) if hasattr(regStr, 'match') else re.match(regStr, oneStr)
                if mch:
                    matched.append(mch)
                else:
                    continue
                
            # check if match is empty 
            if any(matched) > 0:
                value_strings = [mch.group(group) for mch in matched]
                match_strings = [mch.group(0) for mch in matched]
                if asNumber:
                    values = [int(value_string) if len(value_string.split('.')) == 1 else float(value_string) for value_string in value_strings]
                else:
                    values = value_strings
            else:
                raise LookupError("No match found ! regex *{}* doesn't match string *{}*".format(regStr, strings))
            
            resDict = {}
            for key, s in zip(values, match_strings):
                resDict = buildDict(resDict, key, s)
                
            return resDict

        
        else: # for a single string to be matched
            mch = regStr.match(strings) if hasattr(regStr, 'match') else re.match(regStr, strings)
            # check if match is found 
            if mch:
                value_string = mch.group(group)
                match_string = mch.group(0)
            else:
                raise LookupError("No match found ! regex *{}* doesn't match string *{}*".format(regStr, strings))
            # Check convert to number
            if asNumber:
                value = int(value_string) if len(value_string.split('.') == 1) else float(value_string)
            else:
                value = value_string
                
            return dict([(value, match_string)])



    def match(self, strings, group = 1, asNumber = True):
        """
        Match a single or list of regularizations to a single or list of strings
        Return as a dictionary
        """
        if type(self.regex) == list:
            matched_dicts = [self.single_regex_match(regex, strings, group = 1, asNumber = asNumber) for regex in self.regex]
        else:
            matched_dicts = self.single_regex_match(self.regex, strings, group = 1, asNumber = asNumber)
        return matched_dicts

    

    @staticmethod
    def _trace_dict_value(dictIn, trace_list):
        dictOut = dictIn
        for key in trace_list:
            dictOut = dictOut[key]
        return dictOut
        
    @staticmethod
    def _trace_dict_key(dictIn):
        """
        Trace the key path of a nested dictionary
        """
        trace = []
        if type(dictIn) == dict:
            pass
        else:
            return []
        
        for key in dictIn:
            res = [key] + RegMatch._trace_dict_key0(dictIn[key])
            trace.append(res)     
        return trace
                    

    def matchFolder(self, folder_path, asNumber = True, group = 1):
        """
        Match files in the folder content with self.regex
        if two regex are in the self.regex, then the match is done
        in a recursive way, that first regex get matched, and the 2nd
        regex is applied to the match result from the first one.
        """
        
        path = winPathHandler(folder_path)
        searchList = os.listdir(path)
        resDict = {}
        if type(self.regex) == list:
            for i, regex in enumerate(self.regex):
                if i == 0:
                    resDict = self.single_regex_match(regex, searchList, group = group, asNumber = asNumber)
                else:
                    for key in resDict:
                        resDict[key] = self.single_regex_match(regex, resDict[key], group = group, asNumber = asNumber)
        else:
            resDict = self.single_regex_match(self.regex, searchList, group = group, asNumber = asNumber)
        return resDict

    
