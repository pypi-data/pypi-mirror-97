#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A pivot step, which allows you to pivot data
from an existing dataframe along some keys, and then
aggregate other columns with specific functions.
"""
from mitosheet.utils import add_df_to_step, create_new_step, does_sheet_index_exist_within_step
import pandas as pd
from pandas.core.base import DataError
import pandas as pd

from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_aggregation_error,
    make_duplicated_pivot_column_error
)

PIVOT_DISPLAY_NAME = 'Pivoted a Dataframe'

PIVOT_EVENT = 'pivot_edit'
PIVOT_STEP_TYPE = 'pivot'

PIVOT_PARAMS = [
    'sheet_index', # int
    'pivot_rows', # list of column_headers, could be empty
    'pivot_columns', # list of column_headers, could be empty
    'values', # a dict from column_header -> aggregation function
]

def execute_pivot_step(
        curr_step,
        sheet_index,
        pivot_rows,
        pivot_columns,
        values
    ):
    """
    The function responsible for updating the widget state container
    with a new pivot step.

    If it fails part of the way through, deletes the new pivot step entirely.
    """

    # if the sheets don't exist, throw an error
    if not does_sheet_index_exist_within_step(curr_step, sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the pivot by doesn't use any columns that don't exist
    columns_used = set(pivot_rows).union(set(pivot_columns))
    missing_pivot_keys = columns_used.difference(curr_step['column_metatype'][sheet_index].keys())
    if len(missing_pivot_keys) > 0:
        raise make_no_column_error(missing_pivot_keys)

    missing_value_keys = set(values.keys()).difference(curr_step['column_metatype'][sheet_index].keys())
    if len(missing_value_keys) > 0:
        raise make_no_column_error(missing_value_keys)

    # Create a new step
    new_step = create_new_step(curr_step, PIVOT_STEP_TYPE, deep=False)

    # We change the values object here, to make sure that the aggregation functions we use are the ones
    # we want

    # Actually execute the pivoting
    try:
        new_df = _execute_pivot(
            new_step['dfs'][sheet_index], 
            pivot_rows,
            pivot_columns,
            values
        )
    except DataError as e:
        # A data-error occurs when you try to aggregate on a column where the function
        # cannot be applied (e.g. 'mean' on a column of strings)
        print(e)
        # Generate an error informing the user
        raise make_invalid_aggregation_error()
    except ValueError as e:
        # A ValueError occurs when you try to aggregate on a column that is also part of the keys of the pivot table. 
        print(e)
        column_incorrectly_used = str(e).split("\'")[1]
        raise make_duplicated_pivot_column_error(column_incorrectly_used)

    # Add it to the dataframe
    add_df_to_step(new_step, new_df)

    return new_step

def values_to_functions(values):
    """
    Helper function for turning the values mapping sent by the frontend to the values
    mapping to functions that can actually be passed to the pandas pivot function
    """
    new_values = dict()

    for column_header, agg_func_name in values.items():
        # NOTE: this needs to match the values sent from the frontend
        if agg_func_name == 'count unique':
            agg_func = pd.Series.nunique
        else:
            agg_func = agg_func_name
            
        new_values[column_header] = agg_func
    
    return new_values

def _execute_pivot(df, pivot_rows, pivot_columns, values):
    """
    Helper function for executing the pivot on a specific dataframe
    and then aggregating the values with the passed values mapping
    """

    # First, we handle a special case where the only row is also the value
    # the user wants to count. In this case, we
    # This is something that C.M. wants + needs :) 
    if len(pivot_rows) == 1 and len(pivot_columns) == 0 and len(values) == 1 and values == {pivot_rows[0]: 'count'}:
        groupby_obj = df.groupby([pivot_rows[0]], as_index=False)
        return groupby_obj.size()

    # Second, we handle the special case where there are no keys to aggregate on
    # We return an empty dataframe
    if len(pivot_rows) == 0 and len(pivot_columns) == 0 or len(values) == 0:
        return pd.DataFrame(data={})

    values_keys = list(values.keys())

    # Built the args, leaving out any unused values
    args = {}

    if len(pivot_rows) > 0:
        args['index'] = pivot_rows

    if len(pivot_columns) > 0:
        args['columns'] = pivot_columns

    if len(values) > 0:
        args['values'] = values_keys
        args['aggfunc'] = values_to_functions(values)

    pivot_table = df.pivot_table(**args) # type: pd.DataFrame

    # Flatten the column headers
    pivot_table.columns = [
        '_'.join([str(c) for c in col]).strip() if isinstance(col, tuple) else col
        for col in pivot_table.columns.values
    ]

    # flatten the column headers & reset the indexes
    pivot_table = pivot_table.rename_axis(None, axis=1).reset_index()

    return pivot_table

def values_to_functions_code(values):
    """
    Helper function for turning the values mapping sent by the frontend to the values
    mapping that works in generated code. Namely, needs to replay Count Unique with the
    function pd.Series.nunique.
    """
    string_values = f'{values}'
    # NOTE: this needs to match the values sent from the frontend
    # also note that we overwrite the quotes around Count Unique
    return string_values.replace('\'count unique\'', 'pd.Series.nunique')

# Helpful constants for code formatting
TAB = '    '
NEWLINE_TAB = f'\n{TAB}'

def build_args_code(
        pivot_rows,
        pivot_columns,
        values
    ):
    """
    Helper function for building an arg string, while leaving
    out empty arguments. 
    """
    values_keys = list(values.keys())

    args = []
    if len(pivot_rows) > 0:
        args.append(f'index={pivot_rows},')

    if len(pivot_columns) > 0:
        args.append(f'columns={pivot_columns},')

    if len(values) > 0:
        args.append(f'values={values_keys},')
        args.append(f'aggfunc={values_to_functions_code(values)}')
        
    return NEWLINE_TAB.join(args)


def transpile_pivot_step(
        step,
        sheet_index,
        pivot_rows,
        pivot_columns,
        values
    ):
    """
    Transpiles a pivot step to python code!
    """
    new_df_name = f'df{len(step["dfs"])}'


    # First, we handle a special case where the only row is also the value the user wants to count. 
    # In this case, we simply count it! This handles a common case users bump into
    if len(pivot_rows) == 1 and len(pivot_columns) == 0 and len(values) == 1 and values == {pivot_rows[0]: 'count'}:
        return [
            f'groupby_obj = {step["df_names"][sheet_index]}.groupby([\'{pivot_rows[0]}\'], as_index=False)',
            f'{new_df_name} = groupby_obj.size()'
        ]

    
    # Second, we handle the special case where there are no keys or values to aggregate on
    # We return an empty dataframe. 
    if len(pivot_rows) == 0 and len(pivot_columns) == 0 or len(values) == 0:
        return [f'{new_df_name} = pd.DataFrame(data={{}})']

    transpiled_code = []
    
    # Pivot 
    pivot_comment = '# Pivot the data'
    pivot_table_args = build_args_code(pivot_rows, pivot_columns, values)
    pivot_table_call = f'pivot_table = {step["df_names"][sheet_index]}.pivot_table({NEWLINE_TAB}{pivot_table_args}\n)'
    transpiled_code.append(f'{pivot_comment}\n{pivot_table_call}')

    # Flatten column headers. 
    # NOTE: this only needs to happen if there is more than one pivot_column, as the columns
    # will be flat if there are no columns pivoted
    if len(pivot_columns) > 0:
        flatten_comment = '# Flatten the column headers'
        flatten_code = f'pivot_table.columns = [{NEWLINE_TAB}\'_\'.join([str(c) for c in col]).strip() if isinstance(col, tuple) else col{NEWLINE_TAB}for col in pivot_table.columns.values\n]'
        transpiled_code.append(f'{flatten_comment}\n{flatten_code}')

    # Finially, reset the column name, and the indexes!
    reset_index_comment = f'# Reset the column name and the indexes'
    reset_index_code = f'{new_df_name} = pivot_table.rename_axis(None, axis=1).reset_index()'
    transpiled_code.append(f'{reset_index_comment}\n{reset_index_code}')

    return transpiled_code

def describe_pivot(
        sheet_index,
        pivot_rows,
        pivot_columns,
        values,
        df_names=None
    ):

    if df_names is not None:
        new_df_name = f'df{len(df_names)}'
        old_df_name = df_names[sheet_index]
        return f'Pivoted {old_df_name} into {new_df_name}'
    return f'Pivoted dataframe {sheet_index}'


PIVOT_STEP = {
    'step_version': 2,
    'step_display_name': PIVOT_DISPLAY_NAME,
    'event_type': PIVOT_EVENT,
    'step_type': PIVOT_STEP_TYPE,
    'params': PIVOT_PARAMS,
    'saturate': None,
    'execute': execute_pivot_step,
    'transpile': transpile_pivot_step,
    'describe': describe_pivot
}