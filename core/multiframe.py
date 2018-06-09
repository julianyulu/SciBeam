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
# Last-Updated: Sat Jun  9 15:22:11 2018 (-0500)
#           By: yulu
#     Update #: 89
# 

from SciBeam import TOFFrame

class MultiFrame:
    def __init__(self, items):
        self.items = items

    def __getattr__(self, name):
        def inner(*args, **kwargs):
            return TOFFrame().__getattribute__(name)(*args, **kwargs)
        return inner
    
    
            
    
        
        
        
    

