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
# Last-Updated: Sun May 13 14:49:10 2018 (-0500)
#           By: yulu
#     Update #: 12
# 

def format_dict(rawdict, alphabetically = True, digits = 2):
    keys = list(rawdict.keys())
    values = [rawdict[x] for x in keys]
    if alphabetically:
        keys, values = zip(*sorted(zip(keys, values), key = lambda x: x[0]))
    values = ['{:.2f}'.format(x)  if not isinstance(x, str) else x for x in values]
    string = '\n'.join([': '.join([key, str(value)]) for key, value in zip(keys, values)])
    return string
        
    
