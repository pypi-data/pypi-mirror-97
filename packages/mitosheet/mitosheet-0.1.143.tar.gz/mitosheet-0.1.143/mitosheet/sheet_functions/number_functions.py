#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that can be used in a sheet that operate on
numbers.

All functions describe their behavior with a function documentation object
in the function docstring. Function documentation objects are described
in more detail in docs/README.md.

NOTE: This file is alphabetical order!
"""
import functools
import pandas as pd
import numpy as np

from mitosheet.sheet_functions.types.decorators import filter_nans, convert_args_to_series_type, convert_arg_to_series_type, handle_sheet_function_errors
from mitosheet.sheet_functions.sheet_function_utils import fill_series_list_to_max, fill_series_to_length


@handle_sheet_function_errors
@filter_nans
@convert_args_to_series_type('number_series', 'skip', ('default', np.NaN))
def AVG(*argv) -> pd.Series:
    """
    {
        "function": "AVG",
        "description": "Returns the numerical mean value of the passed numbers and series.",
        "examples": [
            "AVG(1, 2)",
            "AVG(A, B)",
            "AVG(A, 2)"
        ],
        "syntax": "AVG(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or series to consider when calculating the average."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or series to consider when calculating the average."
            }
        ]
    }
    """
    # Fill sum to the max length of any series
    argv = fill_series_list_to_max(argv)

    arg_sum = functools.reduce((lambda x, y: x + y), argv) 
    return arg_sum / len(argv)


@handle_sheet_function_errors
@filter_nans
@convert_arg_to_series_type(
    0,
    'number_series',
    'error',
    ('default', np.NaN)
)
@convert_arg_to_series_type(
    1,
    'number_series',
    'error',
    ('default', np.NaN)
)
def CORR(s1, s2) -> pd.Series:
    """
    {
        "function": "CORR",
        "description": "Computes the correlation between two series, excluding missing values.",
        "examples": [
            "=CORR(A, B)",
            "=CORR(B, A)"
        ],
        "syntax": "CORR(series_one, series_two)",
        "syntax_elements": [{
                "element": "series_one",
                "description": "The number series to convert to calculate the correlation."
            }, {
                "element": "series_two",
                "description": "The number series to convert to calculate the correlation."
            }
        ]
    }
    """
    corr = s1.corr(s2, method='pearson')
    return pd.Series(
        [corr] * len(s1)
    )


@handle_sheet_function_errors
@filter_nans
@convert_args_to_series_type('number_series', 'skip', ('default', 1))
def MULTIPLY(*argv) -> pd.Series:
    """
    {
        "function": "MULTIPLY",
        "description": "Returns the product of two numbers.",
        "examples": [
            "MULTIPLY(2,3)",
            "MULTIPLY(A,3)"
        ],
        "syntax": "MULTIPLY(factor1, [factor2, ...])",
        "syntax_elements": [{
                "element": "factor1",
                "description": "The first number to multiply."
            },
            {
                "element": "factor2, ... [OPTIONAL]",
                "description": "Additional numbers or series to multiply."
            }
        ]
    }
    """
    # We make sure all the series are the max length, so the * has something at every index
    argv = fill_series_list_to_max(argv)

    return functools.reduce((lambda x, y: x * y), argv) 


@handle_sheet_function_errors
@filter_nans
@convert_arg_to_series_type(
    0,
    'number_series',
    'error',
    ('default', np.NaN)
)
@convert_arg_to_series_type(
    1,
    'number_series',
    'error',
    ('default', 2),
    optional=True
)
def ROUND(series, decimals=None):
    """
    {
        "function": "ROUND",
        "description": "Rounds a number to a given number of decimals.",
        "examples": [
            "ROUND(1.3)",
            "ROUND(A, 2)"
        ],
        "syntax": "ROUND(value, [decimals])",
        "syntax_elements": [{
                "element": "value",
                "description": "The value or series to round."
            },
            {
                "element": "decimals",
                "description": " The number of decimals to round to. Default is 0."
            }
        ]
    }
    """

    # If no decimals option is passed, round to no decimals
    if decimals is None:
        return series.round()
    
    # Otherwise, fill the decimals to length
    decimals = fill_series_to_length(decimals, series.size)

    return pd.Series(
        [round(num, dec) for num, dec in zip(series, decimals)]
    )


@handle_sheet_function_errors
@convert_arg_to_series_type(
    0,
    'number_series',
    'error',
    ('default', np.NaN)
)
def ABS(series: pd.Series):
    """
    {
        "function": "ABS",
        "description": "Returns the absolute value of the passed number or series.",
        "examples": [
            "ABS(-1.3)",
            "ABS(A)"
        ],
        "syntax": "ABS(value)",
        "syntax_elements": [{
                "element": "value",
                "description": "The value or series to take the absolute value of."
            }
        ]
    }
    """
    return series.abs()


@handle_sheet_function_errors
@filter_nans
@convert_args_to_series_type('number_series', 'skip', ('default', 0))
def SUM(*argv) -> pd.Series:
    """
    {
        "function": "SUM",
        "description": "Returns the sum of the given numbers and series.",
        "examples": [
            "SUM(10, 11)",
            "SUM(A, B, D, F)",
            "SUM(A, B, D, F)"
        ],
        "syntax": "SUM(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or column to add together."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or columns to sum."
            }
        ]
    }
    """
    # Fill sum to the max length of any series
    argv = fill_series_list_to_max(argv)

    return functools.reduce((lambda x, y: x + y), argv) 


@handle_sheet_function_errors
@filter_nans
# NOTE: we set the default to -inf, so that we ignore values that fail to convert
@convert_args_to_series_type('number_series', 'skip', ('default', float("-inf")))
def MAX(*argv) -> pd.Series:
    """
    {
        "function": "MAX",
        "description": "Returns the maximum value among the passed arguments.",
        "examples": [
            "MAX(10, 11)",
            "MAX(Old_Data, New_Data)"
        ],
        "syntax": "MAX(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or column to consider for the maximum value."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or columns to compute the maximum value from."
            }
        ]
    }
    """
    # We make a dataframe out of the series, and take the max between all the columns
    return pd.DataFrame(argv).max()


@handle_sheet_function_errors
@filter_nans
# NOTE: we set the default to inf, so that we ignore values that fail to convert
@convert_args_to_series_type('number_series', 'skip', ('default', float("inf")))
def MIN(*argv) -> pd.Series:
    """
    {
        "function": "MIN",
        "description": "Returns the minimum value among the passed arguments.",
        "examples": [
            "MIN(10, 11)",
            "MIN(Old_Data, New_Data)"
        ],
        "syntax": "MIN(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or column to consider for the minumum value."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or columns to compute the minumum value from."
            }
        ]
    }
    """
    # We make a dataframe out of the series, and take the min between all the columns
    return pd.DataFrame(argv).min()


@handle_sheet_function_errors
@filter_nans
@convert_arg_to_series_type(
    0,
    'number_series',
    'error',
    ('default', np.NaN)
)
def VALUE(series) -> pd.Series:
    """
    {
        "function": "VALUE",
        "description": "Converts a string series to a number series. Any values that fail to convert will return an NaN.",
        "examples": [
            "=VALUE(A)",
            "=VALUE('123')"
        ],
        "syntax": "VALUE(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to convert to a number."
            }
        ]
    }
    """
    return series

# TODO: we should see if we can list these automatically!
NUMBER_FUNCTIONS = {
    'ABS': ABS,
    'AVG': AVG,
    'CORR': CORR,
    'MAX': MAX,
    'MIN': MIN,
    'MULTIPLY': MULTIPLY,
    'ROUND': ROUND,
    'SUM': SUM,
    'VALUE': VALUE
}