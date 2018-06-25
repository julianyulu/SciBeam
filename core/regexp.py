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
# Last-Updated: Mon Jun 25 00:46:25 2018 (-0500)
#           By: yulu
#     Update #: 192
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
    def _trace_dict_key(dictIn, trace_result):
        
        if not type(dictIn) == dict:
            raise TypeError("not dict")
            #return trace_result.append([])
            #return trace_result.append(trace_result[-1].pop())
        else:
            for key in dictIn:
                #trace_result_copy = trace_result.copy()
                print("start: ", dictIn, trace_result)
                
                try:
                    trace_result[-1].append(key)
                except IndexError:
                    print('error')
                    trace_result.append([key])
                maybe_subdict = dictIn[key]
                
                print("end: ", maybe_subdict, trace_result)

                if type(maybe_subdict) == dict:
                    trace_result  = RegMatch._trace_dict_key(maybe_subdict, trace_result)
                else:
                    print('reach leaves')
                    
                    trace_result = trace_result + [trace_result[-1][:-1]]
                    print('trace_result', trace_result)
                    continue
                
            return trace_result

    @staticmethod
    def _trace_dict_key0(dictIn):
        trace = []
        if type(dictIn) == dict:
            pass
        else:
            return []
        
        for key in dictIn:
            res = [key] + RegMatch._trace_dict_key0(dictIn[key])
            trace.append(res)     
        return trace
                    
                    

                
                    
            
        
    def folderMatch(self, folder_path, asNumber = True, group = 1):
        path = self.winPathHandler(folder_path)
        if type(self.regex) == list:
            for i, regex in enumerate(self.regex):
                resDict = {}
                if i == 0:
                    searchList = os.listdir(path)
                    resDict = self.single_regex_match(regex, searchList, group = group, asNumber = asNumber)
                else:
                    for key in resDict:
                        subResDict = self.single_regex_match(regex, resDict[key], group = group, asNumber = asNumber)
                        
        
                
                   
