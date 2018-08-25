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
# Last-Updated: Wed Aug 22 23:55:01 2018 (-0500)
#           By: yulu
#     Update #: 29
#


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq
import warnings

class Gaussian:
    """Class for numerical gaussian funciton application

    A collections of methods for gaussian analysis on the data, such as
    single gaussian function, single gaussian 1d fitting, double gaussian,
    double gaussian fitting, etc.

    """
    @staticmethod
    def gaus(x, A, x0, sigma, offset = 0):
        """gaussian function with or without offset

        General form of a 1D gaussian function, with variable as first
        parameter and other associate parameters followed. Can be used
        for fitting or line plotting after fitting is done.

        The function generally follow the form ::
        y = A * exp(-(x - x0)^2 / (2 * sigma^2)) + offset (optional)

        Handles the case with and without offset seperatelly, since for
        fitting without offset at all one has to force the function to
        be of not offset.

        Parameters
        ----------
        x : float
            variable x in gaussian function
        A : float
            Peak value
        x0 : float
            Center coordinates
        sigma : float
            Standard deviation
        offset : float
            overall offset, default 0

        """

        if offset:
            return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset
        else:
            return A * np.exp(-(x - x0)**2 / (2 * sigma**2))

    @staticmethod
    def gausFit(x, y, offset = False, plot = False):
        """Perform gaussian fit on given data

        Fit data with 1D gausian function ::
        y = a * exp((x - x0)^2 / (2 * sigma)) + y0(optional)

        The function generates initial guesses automatically based on
        given data, the algorithm is based on scipy curve_fit function

        Parameters
        ----------

        x : array-like
            X values of the input data
        y : array-like
            Y values of the input data
        offset : bool
            Wether fit gaussian with offset or not
            Default False
        plot : bool
            Wether plot the fitting result or not
            Default False

        Returns
        -------
        array1
            Array of optmized best fit data [a, x0, sigma, y0]
        array2
            A 4 x 4 covariant matrix of the corresponding optmized data

        Raises
        ------
        RuntimeError
            When optimized parameters not found within max depth of iteration

        """
        # initial guesses
        idxMax = np.argmax(y)
        a0 = y[idxMax]
        x0 = x[idxMax]
        y0 = np.min(y)
        halfWidth = x[idxMax + np.argmin(abs(y[idxMax:] - a0 / 2))] - x[idxMax]

        if offset:
            try:
                popt, pcov = curve_fit(Gaussian.gaus, x, y, p0 = [a0, x0, halfWidth, y0])
            except RuntimeError:
                warnings.warn("curve_fit optimal parameters not found, set as nan")
                popt = np.array([float('NaN')] * 4)
                pcov = np.ones(4, 4) * float('NaN')
        else:
            try:
                popt, pcov = curve_fit(Gaussian.gaus, x, y, p0 = [a0, x0, halfWidth])
            except RuntimeError:
                warnings.warn("curve_fit optimal parameters not found, set as nan")
                popt = np.array([float('NaN')] * 3)
                pcov = np.ones(3, 3) * float('NaN')

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
        """Gaussian function of two independent variables

        Double gaussian function with offset ::
        y = a1 * exp((x - x1)^2 / (2 * sigma1^2) + a2 * exp((x - x2)^2 / (2 * sigma2^2))


        Parameters
        ----------
        x : float
            Input variable for the double gaussian function
        a1 : float
            Amplitude of the first gaussian variable peak
        x1 : float
            Peak center for the first variable gaussian peak
        sigma1 : float
            Sigma vlaues for the two gaussian peaks
        a2 : float
            Amplitude of the second gaussian variable peak
        a2 : float
            Amplitude of the first gaussian variable peak
        x2 : float
            Peak center for the first variable gaussian peak
        sigma2 : float
            Sigma vlaues for the two gaussian peaks
        y0 : float
            Y offset, optional, default y0 = 0

        Returns
        -------
            Numerical value of the double gaussian function

        """
        return a1 * np.exp(-(x - x1)**2/(2 * sigma1**2)) + a2 * np.exp(-(x - x2)**2 / (2 * sigma2 **2)) + y0

    @staticmethod
    def doubleGausFit(x, y, guessPara, offset = False):
        """Two independent variable gaussian fitting

        Fit the data with a double gaussian function base on given
        x, y data and initial guess parameters.

        Unlike the 1D gaussian fitting function, one hase to provide
        initial guess parameters to make sure optimal parameters could
        be found.

        The fitting method is based on  least square method, fitted
        parameters and their covariance matrix is returned.

        Parameters
        ----------
        x : 1D array
            Input data x value
        y : 1D array
            Input data y value
        guessPara: array-like
            Initial guess parameter list[a1, x1, sigma1, a2, x2, sigma2, y0]

        Returns
        -------
        array1
            Fitted parameter array [a1, x1, simga1, a2, x2, simga1]
        array2
            Cnveriance matrix of fitted parameters

        """
        if offset:
            errorFunc = lambda p, x, y: (Gaussian2D.doubleGaus(x, *p) - y)
        else:
            errorFunc = lambda p, x, y: (Gaussian2d.doubleGaus(x, y0 = 0, *p) - y)
            popt, pcov, infodic, mesg, ier= leastsq(errorFunc, guessPara, full_output= True ,args = (x, y))
        if ier < 0:
            raise ValueError("[*] Double gauss fit failed! ")
        return popt, pcov
