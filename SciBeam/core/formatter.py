# formatter.py --- 
# 
# Filename: formatter.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun May 13 14:27:15 2018 (-0500)
# Version: 
# Last-Updated: Fri Jul 20 23:46:23 2018 (-0500)
#           By: yulu
#     Update #: 16
# 

def format_dict(rawdict, alphabetical = True, digits = 2):
    """
    format_dict
    -----------
    Format dictionarys to strings as seperate rows for printing, annotation on plot, etc
    
    [Input]
    rawdict: (dict) raw input dictionary 
    alphabetialy: (bool) if true (default) arrange dict key alphabetical
    digits: (int) number of digits to keep if the value the key is numerical 
    
    [Output]
    (str) formated string in seperate rows
    """

    keys = list(rawdict.keys())
    values = [rawdict[x] for x in keys]
    if alphabetical:
        keys, values = zip(*sorted(zip(keys, values), key = lambda x: x[0]))
    values = [str(digits).join(['{:.','f}']).format(x)  if not isinstance(x, str) else x for x in values]
    string = '\n'.join([': '.join([key, str(value)]) for key, value in zip(keys, values)])
    return string
        
    
