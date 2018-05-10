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
# Last-Updated: Wed May  9 11:34:25 2018 (-0500)
#           By: yulu
#     Update #: 19
# 


class TimeFrame:
    def __init__(self,data):
        #self.__is_mixin =
        self.data = data
        self.time = np.array(self.__data.index)
        self.labels = np.array(self.__data.columns)

    @classmethod
    def __make_descriptor(cls, data):
        return cls(data)
    
    @property
    def data(self):
        return self.__data

    @data.setter(self, data)
    def data(self, data):
        if type(data) == pd.core.frame.DataFrame:
            self.__data == data
        elif type(data) == np.ndarray:
            if data.ndim  == 2:
                if data.shape[0] == 2:
                    t = data[0, :]
                    d = data[1, :]
                elif data.shape[1] == 2:
                    t = data[:,0]
                    d = data[:,1]
                else:
                    print("[*] Too many rows / columns for building a Series")
                    print("[!] Please make sure array is [2 X n] of [n x 2] with time being the first row / column")
                    raise ValueError
                self.__data == pd.DataFrame(data)
            elif data.ndim == 1:
                self.__data == pd.DataFrame(data.reshape(-1, 1))
            else:
                raise ValueError("\n [*] Data array not understand, has to be 1D / 2D array column wise")
            print("[*] Warning: DataFrame time index not set, please mannually set it by TimeFrame.data.index == ...")
        else:
            raise ValueError("\n [*] Data array not understand, has to be 1D / 2D array column wise")

        
    @staticmethod
    def find_time_idx(time, *args):
        """
        Generator of time index for a given time value
        args: can be 1,2,3, or [1,2] or [1,2,3]
        """
        time = np.array(time)
        t_max_gap = np.max(np.diff(time))
        for arg_elem in args:
            
            if hasattr(arg_elem, '__iter__'):
                idx = []
                for t in arg_elem:
                    candi_idx = np.argmin(abs(t - time))
                    if abs(t - time[candi_idx]) > t_max_gap:
                        raise ValueError("[*] Error: find_time_idx didn't find closest match !\n" + 
                                         "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                                         %(t, time[candi_idx]))
                    else: 
                        idx.append(candi_idx)
                        
            else:
                candi_idx = np.argmin(abs(arg_elem - time))
                if abs(t - time[candi_idx]) > t_max_gap:
                    raise ValueError("[*] Error: find_time_idx didn't find closest match !\n" + 
                                     "[!] Searching for time %f while the closest match is %f, you may consider check the unit!"
                                     %(t, time[candi_idx]))
                else:
                    idx = candi_idx
                    
            yield idx
                    

    def selectTimeSlice(self, *args):
        """
        makeSlice
        -------------
        Create descrete time sliced series, if want continus range, use makeTimeRange()
        [Input]
        :args: descrete time slicing values, can use timeSlice(1,2,3,4) or timeSlice([1,2,3,4])
        [Output]
        Series of sliced data
        """
        slice_t = []
        slice_value = []
        for arg_elem in self.find_time_idx(self.time, args):
            if hasattr(arg_elem, '__iter__'):
                for t in arg_elem:
                    slice_t.append(self.time[t])
                    slice_vlaue.append(self.data.iloc[t])
            else:
                slice_t.append(self.time[arg_elem])
                slice_value.append(self.data.iloc[arg_elem])
        slice_series = pd.Series(slice_value, index = slice_t)
                
        return slice_series
