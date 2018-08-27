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
# Last-Updated: Fri Jul 27 20:52:36 2018 (-0500)
#           By: yulu
#     Update #: 48
#

import numpy as np
from scipy.optimize import leastsq, curve_fit
from scipy.fftpack import rfft, irfft
from scipy.integrate import quad
from scibeam.core import base

__all__ = [
    "bandPassFilter",
    "integrate"
    ]


def bandPassFilter(data, tStep = None, lowFreq = 0, highFreq = 1e4):
    """band pass filter based on fourier transform

    Filter the noise in time series data with given frequency range.

    The data has to be in numpy array. If only 1D array is provided, one also
    needs to provide time step size. If 2D array is provided, the 0th column
    will be used to calculate time step size, while the 1st column will be
    treated as the signal value.

    Parameters
    ----------
    data : numpy array
        The input time series data.
        1d array is treated as the signal value, which requires input parameter
        tStep to be not None.
    tStep : float
        Time step size in seconds of the time series data.
        If None (default), 0st columns in data will be treated as time and time
        step size will be extracted from there
    lowFreq :  float
        Lower bound of the bandpass filter, default 0 Hz
    highFreq : float
        Upper bound of the bandpass filter, default 1e4 Hz

    Note
    ----
    The data has to be uniformly sampled, e.g. same time gap between each data
    point, all parameters here are supposed to be SI unit.
    """

    if tStep:
        pass
    else:
        try:
            tStep = data[1, 0] - data[0, 0]
        except IndexError:
            print("Time step value needed if provided is a 1D array")
            raise IndexError
    yf = rfft(data[:,1])
    xf = np.linspace(0, 1 / tStep, len(yf))
    for i, z in enumerate(yf):
        if not lowFreq<= xf[i] < highFreq:
            yf[i] = 0
    iyf = irfft(yf)
    data[:,1] = iyf
    return(data)


def integrate(x = None, y = None, kind = 'numerical', func = None, args = ()):
    """numerical / functional integration

    Perform integration on either numerical data or on a function.

    The numerical intergration is based on given parameter x and y, based on
    numpy function trap; while the functional integration is based on given
    function and numpy function quad.

    Parameters
    ----------
    x : 1D array
        THe x axis values for numerical data, default None
    y : 1D array
        The y axis values for numerical data, default None
    kind : string
        Specify the integration method, options are: 'numerical', 'function'
        default 'numerical'
    func : function
        The function to be integrated, default None
    args
        arguments for function quad
        
    """
    if kind == 'numerical':
        return np.trapz(y, x = x)
    elif kind == 'function':
        return quad(func, x, y,  args = args)[0]
