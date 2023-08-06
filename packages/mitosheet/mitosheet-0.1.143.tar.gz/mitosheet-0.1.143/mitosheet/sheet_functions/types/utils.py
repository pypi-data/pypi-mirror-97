#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Utilities to help with type functions
"""

from typing import Tuple, Union
import pandas as pd
import numpy as np

# Because type(1) = int, thus 1 is a 'number' in the Mito type system
MITO_PRIMITIVE_TYPE_MAPPING = {
    'boolean': [bool],
    'timestamp': [pd.Timestamp],
    'number': [int, float],
    'string': [str],
}


BOOLEAN_SERIES = 'boolean_series'
DATETIME_SERIES = 'datetime_series'
NUMBER_SERIES = 'number_series'
STRING_SERIES = 'string_series'

# NOTE: these are the dtype strings of series used by pandas!
MITO_SERIES_TYPE_MAPPING = {
    BOOLEAN_SERIES: ['bool'],
    DATETIME_SERIES: ['datetime64[ns]'],
    NUMBER_SERIES: ['int64', 'float64'],
    STRING_SERIES: ['str', 'object'],
}

def get_mito_type(obj):

    if isinstance(obj, pd.Series):
        dtype = obj.dtype
        for key, value in MITO_SERIES_TYPE_MAPPING.items():
            if dtype in value:
                return key

    elif isinstance(obj, pd.Timestamp):
        return 'timestamp'
    else:
        obj_type = type(obj)

        for key, value in MITO_PRIMITIVE_TYPE_MAPPING.items():
            if obj_type in value:
                return key

    return None


def get_nan_indexes(*argv): 
    """
    Given the list of arguments to a function, as *argv, 
    returns a list of row indexes that is True iff one of the series 
    params is NaN at that index. Otherwise the index is False

    This function is called by the filter_nan decorator 
    """

    # we find the max length of the args because we are unsure ahead of time which arg 
    # is a series. we need the max_length to construct the boolean index array
    max_length = -1
    for arg in argv:
        # check the type to make sure an error is not thrown for calling len() on an int
        if isinstance(arg, pd.Series) and len(arg) > max_length:
            max_length = len(arg)

    # if there are no series, then:
    #   1. there are no NaN values
    #   2. all of the args are a length of 1
    if max_length == -1:
        return pd.Series([False], dtype='bool')

    nan_indexes = pd.Series([False for i in range(max_length)], dtype='bool')

    # for each row, check for NaN values in the function
    for arg in argv:
        if isinstance(arg, pd.Series): 
            nan_indexes = nan_indexes | pd.isna(arg)

    return nan_indexes

def put_nan_indexes_back(series, nan_indexes):
    """
    This functions takes a series and a boolean index list that is True 
    if the index in the series should be NaN and false if it should
    be left alone. 

    Returns the series with the NaN values put in

    This function is called by the as_types decorator 
    """
    original_length = len(nan_indexes)
    final_series = []
    real_index = 0
    non_nan_index = 0

    while real_index < original_length:
        if nan_indexes[real_index]:
            final_series.append(np.NaN)
        else:
            final_series.append(series[non_nan_index])
            non_nan_index += 1
        real_index +=1

    final_series = pd.Series(final_series)
    return final_series