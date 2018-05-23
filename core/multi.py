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
# Last-Updated: Wed May 23 16:38:22 2018 (-0500)
#           By: yulu
#     Update #: 12
# 

from SciBeam import TOFFrame

class Multi:
    def __init__(self, items, *args, **kwargs):
        self.items = items
        self.__init_frame(*args, **kwargs)


    def __getattr__(self, name):
        if name == '__init_frame':
            name = '__init__'
        print(name)
        def inner(*args, **kwargs):
            return TOFFrame().__getattribute__(name)(*args, **kwargs)
        return inner
    
    
