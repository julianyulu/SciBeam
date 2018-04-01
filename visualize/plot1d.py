# plot1d.py --- 
# 
# Filename: plot1d.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun Apr  1 16:10:55 2018 (-0500)
# Version: 
# Last-Updated: Sun Apr  1 16:21:52 2018 (-0500)
#           By: yulu
#     Update #: 7
# 

import matplotlib.pyplot as plt

def line(x, y, label = None, title = None, subplot = False):
    sharex, sharey, iterxy = False
    if hasattr(x[0], '__iter__'):
        sharex = True
    if hasatr(y[0], '__iter__'):
        sharey = True
    if sharex and shary:
        iterxy = True

    
    if iterxy:
        if subplot:
            fig, ax = plt.subplots(len(x))
        
    
        
    
