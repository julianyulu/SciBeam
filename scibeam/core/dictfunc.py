# dictfuc.py ---
#
# Filename: dictfunc.py
# Description:
#
# Author:    Yu Lu
# Email:     yulu@utexas.edu
# Github:    https://github.com/SuperYuLu
#
# Created: Tue Jun 26 16:15:50 2018 (-0500)
# Version:
# Last-Updated: Tue Aug 28 10:23:47 2018 (-0500)
#           By: yulu
#     Update #: 7
#


def buildDict(init_dict, key, value):
    """build dictionary with key and values on top of existing dict

    Add / set key,value pair to a given dict.
    If the same key exists, combine values to list under the same key
    If no same key exists, creat new key and initialize it to single value

    Parameters
    ----------
    init_dict : dictionary
        original dictionary where new key, value pair to be added to
    key : dictionary key
        The key of dictionary that the value will be associated to
    value : dictionary value
        The value that associated to the key provided

    returns
    -------
    dictionary
        If the given key is already exist in the given dictionary init_dict,
        the function checks if type(init_dict[key]) == list:
        if true, append value the list init_dict[key];
        if false,  change the value of init_dict[key] to be a list
        [init_dict[key], value]

        if the given key is not in init_dict, creat a new key entry and assign
        its value to value (not type list). 

    """

    if key in init_dict:
        if type(init_dict[key]) == list:
            init_dict[key] += [value]
        else:
            init_dict[key] = [init_dict[key]] + [value]

    else:
        init_dict[key] = value

    return init_dict
