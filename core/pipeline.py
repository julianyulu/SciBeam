# pipeline.py --- 
# 
# Filename: pipeline.py
# Description: 
#           pipeline to chain series of process
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu 
# 
# Created: Tue May 15 00:55:01 2018 (-0500)
# Version: 
# Last-Updated: Tue May 15 17:01:17 2018 (-0500)
#           By: yulu
#     Update #: 29
# 

import pandas

class Pipeline:

    def __init__(self, steps, momery = None):
        """
        [(name, func, func_kwargs)]
        """
        
        self.names = steps
        self.tasks = steps
        self.params = steps
        #self._validate_steps()
        self.memory = memory

    @property
    def names(self):
        return self.__names

    @names.setter
    def names(self, steps):
        namelist = []
        
        for i, s in enumerate(steps):
            if len(s) == 1:
                step_name = 'step' + str(i)
            elif len(s) > 1:
                step_name = s[0] if type(s[0])  == str else 'step' + str(i) 
            else:
                raise ValueError("[*] Task cannot be empty !"
                                 "Step %s in pipeline is null" %str(i))
            namelist.append(step_name)
                    
        self.__names = namelist

    @property
    def tasks(self):
        return self.__tasks

    @tasks.setter
    def tasks(self, steps):
        tasklist = []

        for i, t in enumerate(steps):
            if len(t) == 1:
                step_task = t[0]
            elif len(t) > 1:
                step_task = t[1] if type(t[0]) == str else t[0]
            else:
                raise ValueError("[*] Task cannot be empty !"
                                 "Step %s in pipeline is null" %str(i))
        self.__tasks = tasklist

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, steps):
        paramslist = []

        for p in steps:
            if len(p) == 3:
                step_params = p[2]
            elif len(p) == 2 and type(p[1]) == dict:
                step_params = p[1]
            else:
                continue
        return paramslist

            
    def _validate_steps(self):
        names, tasks = zip(*self.steps)
        
        for t in tasks[:-1]:
            if t is None:
                continue

            if not (isinstance(t, pandas.DataFrame) of isinstance(t, pandas.Series)):
                raise TypeError("All pipeline tasks should be instance of padas.Dataframe of pandas.Series"
                                " '%s' (type %s) doesn't" % (t, type(t)))
            
            
    def apply(self, inputs):
        input_value, input_label = zip(*inputs)
        for val in input_value:
            valIn = val
            for task in self.tasks:
                valOut = task(valIn, **self.params)
                valIn = task(valIn, **self.params)
    
