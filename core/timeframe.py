# timeframe.py --- 
# 
# Filename: timeframe.py
# Description: 
#            time data frame analysis
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Sun May  6 14:47:59 2018 (-0500)
# Version: 
# Last-Updated: Sun May  6 15:27:39 2018 (-0500)
#           By: yulu
#     Update #: 12
# 


class TimeFrame:
    def __init__(self,data):
        #self.__is_mixin =
        self.data = data
        self.time = np.array(self.__data.index)
        self.labels = np.array(self.__data.columns)

    @property
    def data(self):
        return self.__data

    @data.setter(self, data)
    def data(self, data):
        if type(data) == pd.core.frame.DataFrame:
            self.__data == data
        elif type(data) == np.ndarray:
            if data.ndim  == 2:
                self.__data == pd.DataFrame(data)
            elif data.ndim == 1:
                self.__data == pd.DataFrame(data.reshape(-1, 1))
            else:
                raise ValueError("\n [*] Data array not understand, has to be 1D / 2D array column wise")
            print("[*] Warning: DataFrame time index not set, please mannually set it by TimeFrame.data.index == ...")
        else:
            raise ValueError("\n [*] Data array not understand, has to be 1D / 2D array column wise")

