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


from scibeam.core.tofframe import (
    TOFFrame,
    read_folder,
    read_regexp_match,
    )

from scibeam.core.tofseries import (
    TOFSeries,
    read_file,
    )

from scibeam.core.plot import (
    PlotTOFSeries,
    PlotTOFFrame,
    )

from scibeam.core.regexp import RegMatch

from scibeam.core.gaussian import Gaussian


