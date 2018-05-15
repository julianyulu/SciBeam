# pipeline.py --- 
# 
# Filename: pipeline.py
# Description: 
#           pipeline to chain series of process
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue May 15 00:55:01 2018 (-0500)
# Version: 
# Last-Updated: Tue May 15 00:56:32 2018 (-0500)
#           By: yulu
#     Update #: 2
# 

class Pipeline:

    def __init__(self, steps, momery = None):
        self.steps = steps
        self._validate_steps()
        self.memory = memory

    
