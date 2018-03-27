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
# Last-Updated: Tue Mar 27 12:06:03 2018 (-0500)
#           By: yulu
#     Update #: 44
# 

import os 
import re
import numpy as np 
from SciBeam.core import base


class Folder(base.Defaults):
    def __init__(self, path):
        self.path = path
        self.__pre_query_result = None
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

    def query(self,regex = base.Defaults.file_regex, path = None,):
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
        if path:
            query_path = path
        else:
            if False:
            """
            if self.__pre_query_result:
                pre_query_result = self.__pre_query_result
                query_result = self.__pre_query_result
                self.__pre_query_result = None 
                #query_path = self.__pre_query_path
                for key in pre_query_result:
                    query_result[key] = {pre_query_result[key]:{}}
                    query_path = base.path_join(self.pre_query_path, pre_query_result[key])
                    query_result[key] = self.query(path = query_path, regex = regex)
                self.__pre_query_result = query_result
                self.__pre_query_path = query_path # <=== this only works for two layers
            """ 
            else:
                query_path = self.path
                    
        files = os.listdir(query_path)
        reg = re.compile(regex)
        result_dict = {}
        for f in files:
            mt = reg.match(f)
            if mt == None:
                continue
            else:
                kwd = mt.group(1)
                whole = mt.group(0)
                result_dict = base.set_dict_key_value(result_dict, kwd, whole)
        return result_dict
    
   
    def queryFolder(self,  layerRegex = '.*(\d+\.\d+).*.lvm$', subfolders = False):
        """
        addressBook
        ----------------
        address book of given path and regexes for sub folders or files 
        
        [Return]
        dictionary of dictionary, 'path' indeication the folder/subfoler path
        """
        rootPath = self.path
        book = {}
        book['path'] = rootPath
        if subfolders:
            regex1, regex2 = layerRegex
            subFolders = [f for f in os.listdir(rootPath) if os.path.isdir(rootPath + f) ]
            if subFolders == []:
                print('Given root path has no subfolders !' )
                raise ValueError
            else:
                for folder in subFolders:
                    matchObj1 = re.match(regex1, folder)
                    if matchObj1:
                        keywd1 = matchObj1.group(1)
                        address1 = matchObj1.group(0)
                        if keywd1 in book:
                            book[keywd1]['path'].append(address1 + '/')
                        else:
                            book[keywd1] = {}
                            book[keywd1]['path'] = address1 + '/'
                            
                        for files in os.listdir(rootPath + folder):
                            matchObj2 = re.match(regex2, files)
                            if matchObj2:
                                keywd2 = matchObj2.group(1)
                                address2 = matchObj2.group(0)
                                if keywd2 in book[keywd1]:
                                    book[keywd1][keywd2].append(address2)
                                else:
                                    #book[keywd1][keywd2] = {}
                                    book[keywd1][keywd2] = [address2]
        else: 
            regex2 = layerRegex if type(layerRegex) == str else layerRegex[0]
            for files in os.listdir(rootPath):
                matchObj = re.match(regex2, files)
                if matchObj:
                    keywd = matchObj.group(1)
                    address = matchObj.group(0)
                    if keywd in book:
                        book[keywd].append(address)
                    else:
                        book[keywd] = [address]
        return book
