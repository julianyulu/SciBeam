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
# Last-Updated: Thu Mar 29 13:27:47 2018 (-0500)
#           By: yulu
#     Update #: 80
# 

import os 
import re
import numpy as np 
from SciBeam.core import base


class Folder(base.Defaults):
    def __init__(self, pathStr):
        self.path = pathStr
        
    @property
    def path(self):
        return self.__path
    
    
    @path.setter
    def path(self, pathStr):
        self.query_result = None
        self.__last_query = None
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
        query filename key value in a endfolder (no subfolders) 
        ------------------
        [input]
        self:
        regex: regular expression for filename keywords query. The regex is meant for 
               full-match, with keyword regex in group(1) 
        [output]
        dictionary of match keywords and corresponding filename 
        """
        if self.__last_query:
            return_result = True
            path = self.__last_query
            result_dict = self.__last_query
            ##
            #potential bug
            self.__last_query = None
            ##
            for last_query_key in path:
                if last_query_key == 'path':
                    continue
                else:
                    query_path = base.pathJoin(path['path'], path[last_query_key])
                    ## potential bug
                    result_dict[last_query_key] = Folder(query_path).query(regex).value()
                    ##
        else:
            return_result = False
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
        
        self.__last_query = result_dict
        self.query_result = result_dict
        return self

    def value(self):
        temp = self.__last_query
        self.__last_query = None
        return temp
    

    
