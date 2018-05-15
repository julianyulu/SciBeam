# regexp.py --- 
# 
# Filename: regexp.py
# Description: 
#            Python regex related functions 
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sat May  5 16:24:14 2018 (-0500)
# Version: 
# Last-Updated: Tue May 15 00:40:19 2018 (-0500)
#           By: yulu
#     Update #: 13
# 

from SciBeam.core.common import Common
import os, re
class RegExp(Common):
    
    def fileMatch(path, regStr, sort = True, asNumber = True):
        """
        Match filenames in path to regStr
        """
        reg  = re.compile(regStr)
        path = Common.winPathHandler(path)
        resultKey = []
        resultFile = []
        if os.path.isdir(path):
            for f in os.listdir(path):
                mch = reg.match(f)
                if mch:
                   key = float(mch.group(1)) if asNumber else mch.group(1)
                   resultKey.append(key)
                   resultFile.append(mch.group(0))
                else:
                    continue
            if sort:
                resultKey, resultFile = list(zip(*sorted(zip(resultKey, resultFile), key = lambda x: x[0])))
            else:
                pass
            
            return list(resultKey), list(resultFile)

        else:
            print("[*]Provided path is not a folder, make sure correct path is provided !")

    
            
                
                   
