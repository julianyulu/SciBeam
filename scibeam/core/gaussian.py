# gaussian.py --- 
# 
# Filename: gaussian.py
# Description: 
#            gaussian analysis and fitting
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue Jun 26 17:18:28 2018 (-0500)
# Version: 
# Last-Updated: Tue Jul 17 17:46:27 2018 (-0500)
#           By: yulu
#     Update #: 17
# 


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class Gaussian:
    
    @staticmethod
    def gaus(x, A, x0, sigma, offset = 0):
        """
        gaussian function with or without offset
        """
        
        if offset: 
            return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset
        else:
            return A * np.exp(-(x - x0)**2 / (2 * sigma**2))

    @staticmethod
    def gausFit(x, y, offset = 0, plot = False):
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
        # initial guesses
        idxMax = np.argmax(y)
        a0 = y[idxMax]
        x0 = x[idxMax]
        y0 = np.min(y)
        halfWidth = x[idxMax + np.argmin(abs(y[idxMax:] - a0 / 2))] - x[idxMax]
        
        if offset:
            popt, pcov = curve_fit(Gaussian.gaus, x, y, p0 = [a0, x0, halfWidth, y0])
        else:
            popt, pcov = curve_fit(Gaussian.gaus, x, y, p0 = [a0, x0, halfWidth])

        if plot:
            plt.plot(x, y, 'o', label = 'raw data')
            plt.plot(x, Gaussian.gaus(x, *popt), '-', label = 'gauss fit')
    
        
        #------------------------------------------------------------
        # leastsq implementation
        # downside: diagnal elements of pcov doesn't give covariance
        #------------------------------------------------------------
        
        #     if offset:
        #         errorFunc = lambda p, x, y: (gaus(x, y0 = 0, *p) - y)
        #     else:
        #         errorFunc = lambda p, x, y: (gaus(x, *p) - y)
        #     popt, pcov, infodic, mesg, ier = leastsq(errorFunc, [a0, x0, halfWidth], full_output = True, args = (x, y))
        #     if ier < 0:
        #         raise ValueError("Gaussian fit failed ")
        
        return popt, pcov


    @staticmethod
    def doubleGaus(x, a1, x1, sigma1, a2, x2, sigma2, y0 = 0):
        """
        - Function: doubleGaus([float]x, [float]a1, [float]x1, [float]sigma1, [float]a2, [float]x2, [float]sigma2, [flaot]y0=0)
        - Description:
              Double gaussian function with offset
              y = a1 * exp((x - x1)^2 / (2 * sigma1^2) + a2 * exp((x - x2)^2 / (2 * sigma2^2))
        - Input:
            - x: [float] input variable for the double gaussian function 
            - a1, a2: [float] Amplitude of the two gaussian peaks
            - x1, x2: [float] Peak center for the two gaussian peaks 
            - sigma1, sigma2: [float] sigma vlaues for the two gaussian peaks
            - y0: [float] y offset, optional, default y0 = 0
        - output
            Calculated double gaussian function
        """
        return a1 * np.exp(-(x - x1)**2/(2 * sigma1**2)) + a2 * np.exp(-(x - x2)**2 / (2 * sigma2 **2)) + y0

    @staticmethod
    def doubleGausFit(x, y, guessPara, offset = False):
        """
        - Function: [array]popt, [array]pcov = doubleGausFit([array]x, [array]y, [array]guessPara)
        - Description: 
              This function to fit the data with a double gaussian function. x, y are the corresponding x, y value of the initial data and initial guess parameters. 
              This function is using least square method to fit the double gaussian function and get the fitting parameters.
        - Input: 
            - x: [array] input data x axis value 
            - y: [array] input data y axis value
            - guessPara: [array/list] initial guess parameter list[a1, x1, sigma1, a2, x2, sigma2, y0]
        - Output:
            - popt: [array] fitted parameter array [a1, x1, simga1, a2, x2, simga1]
            - pcov: [array] corresponding converiance of popt
        """
        if offset: 
            errorFunc = lambda p, x, y: (Gaussian2D.doubleGaus(x, *p) - y)
        else:
            errorFunc = lambda p, x, y: (Gaussian2d.doubleGaus(x, y0 = 0, *p) - y)
            popt, pcov, infodic, mesg, ier= leastsq(errorFunc, guessPara, full_output= True ,args = (x, y))
        if ier < 0:
            raise ValueError("[*] Double gauss fit failed! ")
        return popt, pcov


class Gaussian2D:
    """
    2 dimentional gaussian funtion 
    TO BE IMPLEMENTED
    """
    pass
