# descriptor.py --- 
# 
# Filename: descriptor.py
# Description: 
#            class decorators 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat May  5 23:52:27 2018 (-0500)
# Version: 
# Last-Updated: Wed Jul 18 23:32:05 2018 (-0500)
#           By: yulu
#     Update #: 21
# 


class DescriptorMixin:
    """
    Read-only descriptor for class cross reference 
    """
    
    def __init__(self, descriptor_cls):
        self.descriptor_cls = descriptor_cls
        self.construct_descriptor = descriptor_cls._constructor

    def __get__(self, obj, objtype):
        if obj is None:
            return self.descriptor_cls
        else:
            return self.construct_descriptor(obj)

    def __set__(self, obj, value):
        raise AttributeError("Cannot set value !")

    def __delete__(self, obj):
        raise AttributeError("Cannot delete object!")

    
