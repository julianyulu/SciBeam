# plotseries.py ---
#
# Filename: plotseries.py
# Description:
#
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu
#
# Created: Sun May  6 16:47:06 2018 (-0500)
# Version:
# Last-Updated: Tue Jul 24 23:55:25 2018 (-0500)
#           By: yulu
#     Update #: 315
#

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from .formatter import format_dict
from .gaussian import Gaussian
from . import base
from . import numerical

class PlotTOFSeries:
    """Plot method class for TOFSeries data

    Plot TOFSeries with time as index and another numerical variable as
    column labels. This class makes a copy of the original data so it's
    type safe.

    Designed for using as a mixin class for method chain

    Attributes
    ----------
    __is_mixin : bool
        Indicator of whether the class is been used as mixin class
    data : TOFSeries instance
        The hard copy of TOFSeries instance data
    index_label : string
        The label of index data values
    column_label: string
        The label of columns

    """
    def __init__(self, dataseries, index_label = None, column_label = None):
        self.__is_mixin = base._is_mixin(dataseries)
        self.data = dataseries._make_mixin if self.__is_mixin else dataseries
        self.index_label = index_label
        self.column_label = column_label

    @property
    def data(self):
        """data value as class property

        return the value current stored in data as a property

        Returns
        -------
        TOFSeries instance
            Data that passed to PlotTOFSeries

        """
        return self.__data

    @data.setter
    def data(self, dataseries):
        """data attribute setter

        Set the attribute value of data in a class protected way

        """
        self.__data = dataseries

    @classmethod
    def _constructor(cls, data):
        """PlotTOFSeries class constructor

        Construct class instance using data and other default init values

        Can be used for mixin class as method chain

        """
        return cls(data)


    def plot(self, ax = None, gauss_fit = True, gauss_fit_offset = False, print_fit_params = True, title = None, xlabel = None, ylabel = None, label = None, params_digits = 3, **kwargs):
        """plot 1d time sereis data

        plot the data as 1D plot with optional additional method applied.

        The plot method is using matplotlib and is designed in the way that one
        can plot multiple plot in one, as one can do in matplotlib. Addigionally
        plot receives parameter of ax, which can be used to specify the axis to
        plot, in the situation of multiple subplots this is very useful.

        Additionally, when plotting, one can also specify whether the gaussian
        fitted should be displayed together with the raw data or not, and
        whether print the fitting paraters on the plot.

        Any keyword arguments and be directed passed and the function will pass
        them to it's internal method where matplotlib.pyplot is used.

        ax : matplotlib.axis object
            The axis where the data will be plotted.
            If None(defualt), the data will be ploted on the current existing
            axis (if exists) or create a new axis and plot on it.
        gauss_fit : bool
            If true (default), the data will be fitted with gaussian and the
            fitting line will be plotted together with the raw data.
        gauss_fit_offset : bool
            Only has effect when parameter 'gauss_fit' is set to True
            if True, offset in the data will be considered when performing
            gausssian fit. If False (defalt), the gaussian fit procedure will
            assume the data offset has been properly removed.
        print_fit_params : bool
            Only has effect when parameter 'gauss_fit' is set to True
            If True (default), the fitting parameters from gaussian fit will be
            displayed on the plot; If False, the fitting parameters will not be
            displayed
        params_digits : int
            Only has effect when parameter 'gauss_fit' and 'print_fit_params'
            are both set to be True.
            The number of digits to display when showing the fitting parameters
            default: 3
        title : string
            The title of the plot
        xlabel: string
            The x-axis label
        ylabel : string
            The y-axis label
        label : string
            The label for the data line. Useful for multiple lines on the same
            plot that one may want to add legend to each line.

        """
        if ax is None:
            plt.plot(self.data.index, self.data.values, 'o', **kwargs)

            if gauss_fit:
                popt, pcov = Gaussian.gausFit(x = self.data.index, y = self.data.values, offset = gauss_fit_offset)
                fit_params = {'a': popt[0], 'x0': popt[1], '$\sigma$': popt[2]}
                smoothX = np.linspace(popt[1] - 3* popt[2], popt[1] + 3 * popt[2], 5 * len(self.data.index))
                plt.plot(smoothX, Gaussian.gaus(smoothX, *popt), 'r-')
                plt.figtext(0.95, 0.85, 'fitting parameters:\n' + format_dict(fit_params, digits = params_digits), verticalalignment='top', horizontalalignment='left')

                plt.legend(['data', 'gauss fit'])
            else:
                pass

            # if no gauss_fit, the 2nd label will be muted
            if label: plt.legend([label, 'gauss fit'])
            if ylabel: plt.ylabel(ylabel)
            if xlabel: plt.xlabel(xlabel)
            if title: plt.title(title)

        else:
            ax.plot(self.data.index, self.data.values, 'o', **kwargs)
            if gauss_fit:
                popt, pcov = Gaussian.gausFit(x = self.data.index, y = self.data.values , offset = gauss_fit_offset)
                smoothX = np.linspace(popt[1] - 3* popt[2], popt[1] + 3 * popt[2], 5 * len(self.data.index))
                ax.plot(smoothX, Gaussian.gaus(smoothX, *popt), 'r-', **kwargs)
                ax.legend(['data', 'gauss fit'])
                fit_params = {'a': popt[0], 'x0': popt[1], '$\sigma$': popt[2]}
                plt.figtext(0.95, 0.85, 'fitting parameters:\n' + format_dict(fit_params, digits = params_digits), verticalalignment='top', horizontalalignment='left')
            else:
                pass

            # if no gauss_fit, the 2nd label will be muted, otherwise will overwrite
            if label: ax.legend([label, 'gauss fit'])
            if ylabel: ax.set_ylabel(ylabel)
            if xlabel: ax.set_xlabel(xlabel)
            if title: ax.set_title(title)




class PlotTOFFrame:
    """Plot method class for TOFFrame data

    Plot TOFFrame data with index as time(x labels) and column labels as y label
    . This class makes a copy of the original data so it's data safe.

    Designed for using as a mixin class for method chain

    Attributes
    ----------
    __is_mixin : bool
        Indicator of whether the class is been used as mixin class
    data : TOFFrame instance
        The hard copy of TOFSeries instance data
    index_label : string
        The label of index data values
    column_label: string
        The label of columns

    """
    def __init__(self, dataframe, lowerBound = None, upperBound = None, index_label = None, column_label = None):
        self.__is_mixin = base._is_mixin(dataframe)
        self.data = dataframe._make_mixin if self.__is_mixin else dataframe
        self.index_label = index_label
        self.column_label = column_label

    @property
    def data(self):
        """data value as class property

        return the value current stored in data as a property

        Returns
        -------
        TOFSeries instance
            Data that passed to PlotTOFSeries

        """
        return self.__data

    @data.setter
    def data(self, dataframe):
        """data attribute setter

        Set the attribute value of data in a class protected way

        """
        self.__data = dataframe

    @classmethod
    def _constructor(cls, data):
        """PlotTOFFrame class constructor

        Construct class instance using data and other default init values

        Can be used for mixin class as method chain

        """

        return cls(data)

    def image(self, sideplots = True, contour = False, **kwargs):
        """plot TOFFrame data as image

        Plot the data in TOFFrame as an image, by default, the image uses
        index as its x-axis, uses columns names (must be numbers)  as y-axis

        Additionally the image method adds extral two side plots along x axis
        and y axis to show the integrated signal along a single axis. One can
        also optionally add contour on top of the image plot.

        Parameters
        ----------
        sideplots : bool
            If true (defalt) two side plot will be displayed along x-axis and
            y-axis, which shows the integrated signal along x-axis and y-axis
            correspondingly. If False only the image will be ploted.
        contour : bool
            If true, contour plot will be display on top of the image, the
            contour value is set to be 5 contour levels within 2 time of
            standard deviationas of the signal. If False (default), no contour
            will be displayed.
        kwargs: keyword arguments
            keyword arguments that passed to matplotlib.pyplot.imshow()

        """

        if 'figsize' in kwargs:
            plt.figure(figsize = kwargs.pop('figsize'))
        else:
            plt.figure(figsize = (6,6))

        if sideplots:
            nullfmt = NullFormatter()         # no labels

            # definitions for the axes
            left, width = 0.1, 0.65
            bottom, height = 0.1, 0.65
            bottom_h = left_h = left + width + 0.02

            rect_img = [left, bottom, width, height]
            rect_distx = [left, bottom_h, width, 0.2]
            rect_disty = [left_h, bottom, 0.2, height]
            rect_cax = [left_h, bottom_h, 0.1, 0.2]

            # start with a rectangular Figure
            axImg = plt.axes(rect_img)
            axDistrx = plt.axes(rect_distx)
            axDistry = plt.axes(rect_disty)
            cax = plt.axes(rect_cax)
            # no labels
            axDistrx.xaxis.set_major_formatter(nullfmt)
            axDistry.yaxis.set_major_formatter(nullfmt)


            areaDataY = [np.trapz(x = self.data.index, y = self.data[x]) for x in self.data]
            areaDataX = [np.trapz(x = self.data.columns, y = self.data.loc[x,:]) for x in self.data.index]
            axDistrx.plot(self.data.index, areaDataX)
            axDistry.plot(areaDataY, self.data.columns)
            #axDistry.invert_yaxis() # don't need to invert anymore

            # has to flip data so that lower position starts from lower part of the image
            im = axImg.imshow(np.flipud(self.data.values.T),
                            **kwargs,
                            aspect = 'auto',
                            extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],

                            )
            axImg.set_xlabel(self.index_label if self.index_label else 'Time of flight')
            axImg.set_ylabel(self.column_label if self.column_label else 'Position')
            cbar = plt.colorbar(im,  cax = cax)
            #cbar.ax.set_ylabel('Signal')
        else:
            im = plt.imshow(np.flipud(self.data.values.T),
                            **kwargs,
                            aspect = 'auto',
                            extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],

                            )
            plt.xlabel(self.index_label if self.index_label else 'Time of flight')
            plt.ylabel(self.column_label if self.column_label else 'Position')
            cbar = plt.colorbar(im)
            #cbar.ax.set_ylabel('Signal')

        if contour:
            if sideplots:
                self.contour(colors = 'w', ax = axImg, title = '', xlabel = '', ylabel = '')
            else:
                self.contour(colors = 'w', title = '', xlabel = '', ylabel = '')


    def contour(self, n_contours = 5, n_sigma = 2, xlabel = 'time', ylabel = 'value', title = 'contour plot', label = None,
           ax = None, image = False, **kwargs):
        """contour plots on TOFFrame data

        Plot contours on the TOFFrame data. Same as the 'image' method, the
        contour plot by default uses index as its x-axis, uses columns names
        (must be numbers)  as y-axis.

        The contour levels are based on multiples of the standard deviation
        as from gausssian fitting. By default only 5 contour levels evenly
        space between 2 standard deviations and 0.2 standard deviations are
        ploted.

        Note
        -----
            THe highest contour level is set to be 0.2 standard deviation away
            from the peak value so that it is still visiable on the contour
            plot

        Parameters
        ----------
        n_contours : int
            number of contour levels to plot, default 2
            The n_contours contour are evenly spaced between 2 standard
            deviations and 0.2 standard deviations are ploted.
        n_sigma : int
            multiples of standard deviation from the peak that the furthest
            contour level from peak center should be. This basically set the
        

        """
        popt = self.data.peak.height().gausFit()[0]
        n_sigma_levels = Gaussian.gaus(popt[1] + np.linspace(n_sigma, 0.2 ,  n_contours)* popt[2], *popt)

        if ax:
            ax.contour(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            if image:
                ax.imshow(np.flipud(self.data.values.T),
                          aspect = 'auto',
                          extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],
                         )



        else:
            plt.contour(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            if image:
                plt.imshow(np.flipud(self.data.values.T),
                          aspect = 'auto',
                          extent=[self.data.index[0], self.data.index[-1], self.data.columns[0], self.data.columns[-1]],
                         )

    def contourf(self, n_contours = 5, n_sigma = 2, xlabel = 'time', ylabel = 'value', title = 'contour plot', label = None,
           ax = None, **kwargs):
        """
        contourf plots for 2D self.data

        """
        popt = self.data.peak.height().gausFit()[0]
        n_sigma_levels = Gaussian.gaus(popt[1] + np.linspace(n_sigma, 0.2 ,  n_contours)* popt[2], *popt)
        if ax:
            ax.contourf(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        else:
            plt.contourf(self.data.index, self.data.columns, self.data.T, n_sigma_levels, **kwargs)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
