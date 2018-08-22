# __init__.py ---
#
# Filename: __init__.py
# Description:
#            Module scibeam __init__
#
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu
#
# Created: Sun Mar 25 16:04:08 2018 (-0500)
# Version:
# Last-Updated: Sun Aug 19 15:03:24 2018 (-0500)
#           By: yulu
#     Update #: 53
#

"""Scibeam

For scientific time series analysis and visualization.

"""

name = "scibeam"



from .core.tofframe import (
    TOFFrame,
    read_folder,
    read_regexp_match,
    )

from .core.tofseries import (
    TOFSeries,
    read_file,
    )

from .core.plot import (
    PlotTOFSeries,
    PlotTOFFrame,
    )

from .core.regexp import RegMatch

from .core.gaussian import Gaussian
