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
# Last-Updated: Sun Jun 24 18:21:05 2018 (-0500)
#           By: yulu
#     Update #: 76
# 

from SciBeam.core.common import Common
from SciBeam.core import base
import os, re
class RegMatch(Common):
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
                resDict = base.buildDict(resDict, key, s)
                
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
        if type(self.regex) == list:
            matched_dicts = [self.single_regex_match(regex, strings, group = 1, asNumber = asNumber) for regex in self.regex]
        else:
            matched_dicts = self.single_regex_match(self.regex, strings, group = 1, asNumber = asNumber)
        return matched_dicts
        

    ### -----not finished below -----
    @staticmethod
    def folderMatch(regStr, path, asNumber = True, group = 1):
        path = self.winPathHandler(path)
        is_multi_regex = True if type(regStr) == list else False
                
        if is_multi_regex:
            for i, regex in enumerate(regStr):
                resDict = {}
                if i == 0:
                    searchList = os.listdir(path)
                    resDict = RegExp.match(regex, searchList, asNumber = asNumber, group = group)
                else:
                    for key in resDict:
                        subResDict = RegExp.match(regex, resDict[key], asNumber = asNumber, group = group)
                        resDict[key] = subResDict
            return resDict
        
        else:
            resDict = RegExp.match(regStr, os.listdir(path), asNumber = asNumber, group = group)
                
                    
                    
                
        
    @staticmethod 
    def fileMatch(path, regStr, sort = True, asNumber = True, group = 1):
        """
        Match filenames in path to regStr
        """
        reg  = re.compile(regStr)
        path = self.winPathHandler(path)
        resultValue = []
        resultFile = []
        if os.path.isdir(path):
            for f in os.listdir(path):
                match_value, match_string = RegExp.match(reg, f, asNumber = asNumber, group = group)
                resultValue.append(match_value)
                resultFile.append(match_string)
            if sort:
                resultValue, resultFile = list(zip(*sorted(zip(resultValue, resultFile), key = lambda x: x[0])))
            else:
                pass
            
            return list(resultValue), list(resultFile)

        else:
            print("[*]Provided path is not a folder, make sure correct path is provided !")

    
        
    
                
                   
