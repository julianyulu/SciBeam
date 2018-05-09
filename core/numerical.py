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
# Last-Updated: Tue May  8 23:54:28 2018 (-0500)
#           By: yulu
#     Update #: 31
# 

import numpy as np
from scipy.optimize import leastsq
from scipy.fftpack import rfft, irfft
from scipy.integrate import quad
from SciBeam.core import base

__all__ = [
    "gaus",
    "gausFit",
    "doubleGaus",
    "doubleGausFit"
    ]


def gaus(x, A, x0, sigma, y0 = 0):
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + y0

def gausFit(x, y, offset = False):
    """
    - Functions: [float, array]popt, [float, array]pcov = gausFit([2D array]data)
    - Description:
              This function is to fit data with 1D gausian equation:
                  y = a * exp((x - x0)^2 / (2 * sigma)) + y0
            it's calling funciton gaus and curve_fit (from scipy.optimize lib) to fit the 
            data. Sometimes (merely) it cannot find the optimized prarameters to fit the 
            data, that could be due to the range of peak giving in variable 'data'. It returns
            optimized parameters and their error.
    - Input:
            - x, y: 2D array, column gives x, while column gives y
    - Output: 
            - popt: [float,array] array of optmized data [a, x0, sigma, y0]
            - pcov: [float, array] covariant of the corresponding optmized data 
    
    """
    idxMax = np.argmax(y)
    a0 = y[idxMax]
    x0 = x[idxMax]
    
    halfWidth = x[idxMax + np.argmin(abs(y[idxMax:] - a0 / 2))] - x[idxMax]
    if offset:
        errorFunc = lambda p, x, y: (gaus(x, y0 = 0, *p) - y)
    else:
        errorFunc = lambda p, x, y: (gaus_noOffset(x, *p) - y)
    popt, pcov, infodic, mesg, ier = leastsq(errorFunc, [a0, x0, halfWidth], full_output = True, args = (x, y))
    if ier < 0:
        raise ValueError("Gaussian fit failed ")
    return popt, pcov


def doubleGaus(x, a0, x0, sigma0, a1, x1, sigma1, y0 = 0):
    """
    - Function: doubleGaus([float]x, [float]a0, [float]x0, [float]sigma0, [float]a1, [float]x1, [float]sigma1, [flaot]y0=0)
    - Description:
              Double gaussian function with offset
              y = a0 * exp((x - x0)^2 / (2 * sigma0^2) + a1 * exp((x - x1)^2 / (2 * sigma1^2))
    - Input:
            - x: [float] input variable for the double gaussian function 
            - a0, a1: [float] Amplitude of the two gaussian peaks
            - x0, x1: [float] Peak center for the two gaussian peaks 
            - sigma0, sigma1: [float] sigma vlaues for the two gaussian peaks
            - y0: [float] y offset, optional, default y0 = 0
    - output
            Calculated double gaussian function
    """
    return a0 * np.exp(-(x - x0)**2/(2 * sigma0**2)) + a1 * np.exp(-(x - x1)**2 / (2 * sigma1 **2)) + y0


def doubleGausFit(x, y, guessPara, offset = False):
    """
    - Function: [array]popt, [array]pcov = doubleGausFit([array]x, [array]y, [array]guessPara)
    - Description: 
              This function to fit the data with a double gaussian function. x, y are the corresponding x, y value of the 
            initial data and initial guess parameters. 
              This function is using least square method to fit the double gaussian function and get the fitting parameters.
    - Input: 
            - x: [array] input data x axis value 
            - y: [array] input data y axis value
            - guessPara: [array/list] initial guess parameter list[a0, x0, sigma0, a1, x1, sigma1, y0]
    - Output:
            - popt: [array] fitted parameter array [a0, x0, simga0, a1, x1, simga1]
            - pcov: [array] corresponding converiance of popt
              
    
    """
    if offset: 
        errorFunc = lambda p, x, y: (doubleGaus(x, *p) - y)
    else:
        errorFunc = lambda p, x, y: (doubleGaus(x, y0 = 0, *p) - y)
    popt, pcov, infodic, mesg, ier= leastsq(errorFunc, guessPara, full_output= True ,args = (x, y))
    if ier < 0:
        raise ValueError("[*] Double gauss fit failed! ")
return popt, pcov


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
    if kind == 'numerical':
        return np.trapz(y, x = x)
    elif kind == 'function':
        return quad(func, low, high, args = args)[0]

