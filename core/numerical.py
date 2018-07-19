# numerical.py --- 
# 
# Filename: numerical.py
# Description: 
# 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue May  8 23:19:52 2018 (-0500)
# Version: 
# Last-Updated: Thu Jul 19 11:10:00 2018 (-0500)
#           By: yulu
#     Update #: 43
# 

import numpy as np
from scipy.optimize import leastsq, curve_fit
from scipy.fftpack import rfft, irfft
from scipy.integrate import quad
from SciBeam.core import base

__all__ = [
    "bandPassFilter",
    "integrate"
    ]


def bandPassFilter(data, tStep = None, lowFreq = 0, highFreq = 1e4):
    """
    band pass filter based on fourier transform 
    """
    
    if tStep:
        pass
    else:
        tStep = data[1, 0] - daa[0, 0]
    yf = rfft(data[:,1])
    xf = np.linspace(0, 1 / tStep, len(yf))
    for i, z in enumerate(yf):
        if not lowFreq<= xf[i] < highFreq:
            yf[i] = 0
    iyf = irfft(yf)
    data[:,1] = iyf
    return(data)


def integrate(x = 0, y = 0, kind = 'numerical', func = None, low = None, high = None, args = ()):
    """
    numerical / function integration using numpy trapz / scipy quad
    """
    if kind == 'numerical':
        return np.trapz(y, x = x)
    elif kind == 'function':
        return quad(func, low, high, args = args)[0]


