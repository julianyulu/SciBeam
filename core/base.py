# base.py --- 
# 
# Filename: base.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun Mar 25 22:03:54 2018 (-0500)
# Version: 
# Last-Updated: Sat May  5 13:43:44 2018 (-0500)
#           By: yulu
#     Update #: 43
# 
import os 

class Defaults:

    # Top level
    #-----------------
    data_file_extenstion = '.lvm'
    data_file_num_column = 2
    # Lower level
    # ----------------
    subfolder_regex = '.*(\d+\.?\d+).*'
    file_regex = '.*_(\d+\.?\d+).*' + data_file_extenstion + '$'

    # Unit tests
    

def buildDict(init_dict, key, value):
    """
    Add / set key,value pair to a given dict.
    If the same key exists, combine values to list 
    If no same key exists, creat new key and initialize the value 
    -----------------
    [Input]
    init_dict: original dictionary where new key, value pair to be added to 
    key: key of dictionary
    value: value corresponding to the key
    
    [output]
    new_dict: dictionary from init_dict with updated key,values 
    """
    
    if key in init_dict:
        if type(init_dict[key]) == list:
            init_dict[key] += [value]
        else:
            init_dict[key] = [init_dict[key]] + [value]

    else:
        init_dict[key] = value

    return init_dict    

    
def pathJoin(*args):
    """
    Join multiple paths for windows / linux and take care of the 
    slashes by the end
    """

    num_path = len(args)
    result_path = ''
    for pathStr in args:
        tempPath = pathStr.replace('\\','/')
        #tempPath = tempPath[1:] if tempPath[0] == '/' else tempPath
        result_path += tempPath if tempPath[-1] == '/' else tempPath + '/'
        result_path.replace('//', '/') # incase the are two '/' 
        if os.path.isdir(result_path):
            pass
        else:
            result_path = result_path[:-1]
    return result_path

    # if os.path.isdir(result_path):
    #     return result_path
    # else:
    #     print("[!] Combined path %s is not recognized as a directory !" %result_path)
    #     print("If using Windows path, make sure using *raw* strings\n",
    #           "e.g.: r'C:\folder\folder\folder'  ")
    #     raise FileNotFoundError
    
            
            
            
