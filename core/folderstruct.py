# FolderStruct.py --- 
# 
# Filename: FolderStruct.py
# Description: 
#            Class FolderStruct
#            ---------------------
#            For folder structure analysis, regex indexing,
#            file group and loading.
#
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Fri Mar 23 23:02:05 2018 (-0500)
# Version: 0.1
# Last-Updated: Sun Apr  1 17:51:20 2018 (-0500)
#           By: yulu
#     Update #: 98
# 

import os 
import re
import numpy as np 
from SciBeam.core import base


class Folder(base.Defaults):
    def __init__(self, pathStr):
        self.path = pathStr
        self.fileDict = None


    @property
    def path(self):
        return self.__path
        
    @path.setter
    def path(self, pathStr):
        if os.path.isdir(pathStr):
            tempPath = pathStr.replace('\\','/')
            self.__path = tempPath if tempPath[-1] == '/' else tempPath + '/'
        else:
            print("[!] %s is no recognized as a directory !" %pathStr)
            print("If using Windows path, make sure using *raw* strings\n",
                  "e.g.: r'C:\folder\folder\folder'  ")
            raise FileNotFoundError

    def query(self,regex = base.Defaults.file_regex):
        """
        single folder query based on python regex group1
        ------------------
        [input]
        self:
        regex: regular expression for filename keywords query. The regex is meant for 
               full-match, with keyword regex in group(1) 
        [output]
        dictionary of match keywords and corresponding filename 
        """
        result_dict = {}
        result_dict['path'] = self.path
        files = os.listdir(self.path)
        reg = re.compile(regex)
        for f in files:
            mt = reg.match(f)
            if mt == None:
                continue
            else:
                kwd = mt.group(1)
                whole = mt.group(0)
                result_dict = base.buildDict(result_dict, kwd, whole)
        self.fileDict = result_dict
        return self


class FolderTools:
    def __init__(self):
        pass

    @staticmethod
    def query(path, regex = base.Defaults.file_regex):
        result_dict = {}
        result_dict['path'] = path
        files = os.listdir(path)
        reg = re.compile(regex)
        for f in files:
            mt = reg.match(f)
            if mt == None:
                continue
            else:
                kwd = mt.group(1)
                whole = mt.group(0)
                result_dict = base.buildDict(result_dict, kwd, whole)
        fileDict = result_dict
        return fileDict

    def query_gen(path, regex = base.Defaults.file_regex):
        files = os.listdir(path)
        reg = re.compile(regex)
        for f in files:
            mt = reg.match(f)
            if mt == None:
                continue
            else:
                kwd = mt.group(1)
                whole = mt.group(0)
                yield base.pathJoin(path, whole)
        
        

    
    
