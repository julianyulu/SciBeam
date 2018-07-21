# dictfuc.py --- 
# 
# Filename: dictfunc.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue Jun 26 16:15:50 2018 (-0500)
# Version: 
# Last-Updated: Tue Jun 26 16:28:38 2018 (-0500)
#           By: yulu
#     Update #: 6
# 


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

    
