# FolderHierarchy.py --- 
# 
# Filename: FolderHierarchy.py
# Description: 
#            Class FolderHierarchy
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
# Last-Updated: Fri Mar 23 23:04:12 2018 (-0500)
#           By: yulu
#     Update #: 4
# 

import os 
import re
import numpy as np 

class FolderHierarchy:
    def __init__(self, path):
        self.path = path
    
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
            
    def queryType(self, qType = float, extension = '.lvm'):
        regMap = {
            float: '\d+\.?\d+',
            int: '\d+',
            str: '\s'
        }
        if type(qType) == type:
            rgx = re.compile(regMap[qType])
            kwds = [[rgx.findall(self.path), file] for file in os.listdir(self.path) if file.endswith(extension)]
            return kwds
        else:
            print('please input a python type (not string), e.g. float, int, str, etc.')
    
    def querykwds(self, regex = '.*(\d+\.\d+).*.lvm$'):
        files = os.listdir(self.path)
        reg = re.compile(regex)
        kwdList = []
        fileList = []
        for f in files:
            mt = reg.match(f)
            if mt == None:
                continue
            else:
                kwdList.append(mt.group(1))
                fileList.append(f)
        return(kwdList, fileList)
    
   
    def addressBook(self,  layerRegex = '.*(\d+\.\d+).*.lvm$', subfolders = False):
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

    @staticmethod
    def loadData(fileName, ncol = 2):
        data = np.fromfile(fileName,  sep = '\t').reshape(-1,ncol)
        return data

        
    @staticmethod
    def loadAddressBook(addressDict, ncol = 2):
        dataBook = {}
        print("[*] In folder %s, loading..." %addressDict['path'])
        for key1 in sorted(list(addressDict.keys() - ['path'])):
            path = addressDict['path']
            try:
                subpath = dataBook[key1]['path']
            except KeyError:
                subpath = None
                pass
            if subpath:
                print('Key1: %s,  Key2:' %key1, end=" ")
                dataBook[key1] = {}
                for key2 in sorted(list(addressDict[key1].keys() - ['path'])):
                    print(key2, end = " ")
                    dataBook[key1][key2] = []
                    for fileName in addressDict[key1][key2]:
                        data = np.fromfile(path + subpath + fileName,  sep = '\t').reshape(-1,ncol)
                        #data = np.loadtxt(path + subpath + fileName, skiprows = 30)
                        dataBook[key1][key2].append(data)
                print('\n')
                    else:
                print('%s' %key1, end = " ")
                dataBook[key1] = []               
                for fileName in addressDict[key1]:
                    data = np.fromfile(path + fileName,  sep = '\t').reshape(-1,2)
                    #data = np.loadtxt(path + fileName, skiprows = 30)
                    dataBook[key1].append(data)
        return dataBook

