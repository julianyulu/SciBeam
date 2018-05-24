# multi.py --- 
# 
# Filename: multi.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue May 15 17:37:29 2018 (-0500)
# Version: 
# Last-Updated: Wed May 23 18:01:03 2018 (-0500)
#           By: yulu
#     Update #: 21
# 

from SciBeam import TOFFrame

class MultiFrame:
    def __init__(self, items, *args, **kwargs):
        self.items = items
        
    def __getattr__(self, name):
        def inner(*args, **kwargs):
            return TOFFrame().__getattribute__(name)(*args, **kwargs)
        
    



