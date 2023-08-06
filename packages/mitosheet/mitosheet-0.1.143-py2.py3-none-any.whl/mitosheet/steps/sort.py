#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A sort step, which allows you to sort a df based on some key column
"""
from mitosheet.utils import create_new_step, does_sheet_index_exist_within_step
from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_sort_error
)

SORT_DISPLAY_NAME = 'Sorted a Column'

SORT_EVENT = 'sort_edit'
SORT_STEP_TYPE = 'sort'

SORT_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # column to sort
    'sort_direction' # string either 'ascending' or 'descending'
]

# CONSTANTS USED IN THE SORT STEP ITSELF
ASCENDING = 'ascending'
DESCENDING = 'descending'

def execute_sort(
        curr_step,
        sheet_index,
        column_header,
        sort_direction,
    ):
    """
    sorts an existing sheet with the given sort_direction on the column_header
    """
    # if the sheet doesn't exist, throw an error
    if not does_sheet_index_exist_within_step(curr_step, sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the sorted column exists 
    missing_column = set([column_header]).difference(curr_step['column_metatype'][sheet_index].keys())
    if len(missing_column) > 0: 
        raise make_no_column_error(missing_column)

    # If no errors we create a new step for this sort
    new_step = create_new_step(curr_step, SORT_STEP_TYPE)

    # execute on real dataframes
    new_step['dfs'][sheet_index] = _execute_sort(
        new_step['dfs'][sheet_index], 
        column_header,
        sort_direction
    )

    return new_step

def _execute_sort(
        df,
        column_header,
        sort_direction,
    ):
    """
    Executes a sort on the given df, by sorting the column named 
    column_header in sort_direction (ascending or descending)
    """

    try: 
        new_df = df.sort_values(by=column_header, ascending=(sort_direction == ASCENDING), na_position='first')
        return new_df.reset_index(drop=True)
    except TypeError as e:
        # A NameError occurs when you try to sort a column with incomparable 
        # dtypes (ie: a column with strings and floats)
        print(e)
        # Generate an error informing the user
        raise make_invalid_sort_error(column_header)

def transpile_sort(
        step,
        sheet_index,
        column_header,
        sort_direction
    ):
    """
    Transpiles a sort step to Python code. 
    """
    # sort the dataframe
    df_name = step["df_names"][sheet_index]
    sort_line = f'{df_name} = {df_name}.sort_values(by=\'{column_header}\', ascending={sort_direction == ASCENDING}, na_position=\'first\')'
    reset_index_line = f'{df_name} = {df_name}.reset_index(drop=True)'

    return [sort_line, reset_index_line]


def describe_sort(
        sheet_index,
        column_header,
        sort_direction,
        df_names=None,
    ):
    
    if df_names is not None:
        df_name = df_names[sheet_index]
        return f'Sorted {column_header} in {df_name} in {sort_direction} order'
    return f'Sorted {column_header} in {sort_direction} order'


SORT_STEP = {
    'step_version': 1,
    'step_display_name': SORT_DISPLAY_NAME,
    'event_type': SORT_EVENT,
    'step_type': SORT_STEP_TYPE,
    'params': SORT_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_sort,
    'transpile': transpile_sort,
    'describe': describe_sort
}