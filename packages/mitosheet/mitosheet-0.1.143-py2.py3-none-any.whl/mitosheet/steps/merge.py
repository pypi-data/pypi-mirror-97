#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A merge step, which allows you to merge two dataframes
together.
"""
from mitosheet.utils import add_df_to_step, create_new_step, does_sheet_index_exist_within_step
from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
)

MERGE_DISPLAY_NAME = 'Merged Two Dataframes'

MERGE_EVENT = 'merge_edit'
MERGE_STEP_TYPE = 'merge'

MERGE_PARAMS = [
    'sheet_index_one', # First df to merge
    'merge_key_one', # Key to merge on
    'selected_columns_one', # The columns to keep from the first sheet 
    'sheet_index_two', # Second df to merge
    'merge_key_two', # The second key to merge on 
    'selected_columns_two', # The columns to keep from the second sheet
]

def execute_merge_step(
        curr_step,
        sheet_index_one: int,
        merge_key_one: str,
        selected_columns_one,
        sheet_index_two: int,
        merge_key_two: str,
        selected_columns_two
    ):
    """
    Creates a new sheet by merging sheet_index_one and sheet_index_two together
    on the keys merge_key_one and merge_key_two respectively. 
    
    Note, that merge does not treat np.NaN = np.NaN, so NaN keys won't be matched 
    with anything, making any column in the second sheet NaN for that row in the resulting merged sheet.
    
    The merged sheet will contain all of the columns from sheet_index_one 
    and sheet_index_two

    If either merge key does not exist, it raises an exception.
    """
    # if the sheets don't exist, throw an error
    if not does_sheet_index_exist_within_step(curr_step, sheet_index_one):
        raise make_no_sheet_error(sheet_index_one)

    if not does_sheet_index_exist_within_step(curr_step, sheet_index_two):
        raise make_no_sheet_error(sheet_index_two)

    # We check that the merge doesn't use any columns that don't exist
    missing_sheet_one_key = {merge_key_one}.difference(curr_step['column_metatype'][sheet_index_one].keys())
    if any(missing_sheet_one_key):
        raise make_no_column_error(missing_sheet_one_key)

    missing_sheet_two_key = {merge_key_two}.difference(curr_step['column_metatype'][sheet_index_two].keys())
    if any(missing_sheet_two_key):
        raise make_no_column_error(missing_sheet_two_key)

    # If no errors we create a new step for this merge
    new_step = create_new_step(curr_step, MERGE_STEP_TYPE, deep=False)

    new_df = _execute_merge(
        new_step,
        new_step['dfs'], 
        sheet_index_one,
        merge_key_one,
        selected_columns_one,
        sheet_index_two,
        merge_key_two,
        selected_columns_two
    )    

    # Add this dataframe to the current step!
    add_df_to_step(new_step, new_df)

    return new_step

def _execute_merge(
        new_step,
        dfs, 
        sheet_index_one,
        merge_key_one, 
        selected_columns_one,
        sheet_index_two,
        merge_key_two,
        selected_columns_two
    ):
    """
    Executes a merge on the sheets with the given indexes, merging on the 
    given keys, and only keeping the selection columns from each df.
    
    TODO: figure out how to simulate VLOOKUP style work better here...
    """
    # We drop duplicates to avoid pairwise duplication on the merge.
    temp_df = dfs[sheet_index_two].drop_duplicates(subset=merge_key_two)

    # Then we delete all the columns from each we don't wanna keep
    deleted_columns_one = set(dfs[sheet_index_one].keys()).difference(set(selected_columns_one))
    deleted_columns_two = set(dfs[sheet_index_two].keys()).difference(set(selected_columns_two))

    df_one_cleaned = dfs[sheet_index_one].drop(deleted_columns_one, axis=1)
    df_two_cleaned = temp_df.drop(deleted_columns_two, axis=1)

    # Finially, we perform the merge!
    df_one_name = new_step['df_names'][sheet_index_one]
    df_two_name = new_step['df_names'][sheet_index_two]
    # We make sure the suffixes aren't the same, as otherwise we might end up with 
    # one df with duplicated column headers
    suffix_one = df_one_name
    suffix_two = df_two_name if df_two_name != df_one_name else f'{df_two_name}_2'

    return df_one_cleaned.merge(df_two_cleaned, left_on=[merge_key_one], right_on=[merge_key_two], how='left', suffixes=[f'_{suffix_one}', f'_{suffix_two}'])

def transpile_merge_step(
        step,
        sheet_index_one,
        merge_key_one, 
        selected_columns_one,
        sheet_index_two,
        merge_key_two,
        selected_columns_two
    ):
    """
    Transpiles a merge step to python code!
    """

    # update df indexes to start at 1
    df_one_name = step['df_names'][sheet_index_one]
    df_two_name = step['df_names'][sheet_index_two]
    df_new_name = step['df_names'][len(step['dfs']) - 1]

    # Now, we build the merge code (starting with the code for dropping duplicates)
    merge_code = [
        f'temp_df = {df_two_name}.drop_duplicates(subset=\'{merge_key_two}\')',
    ]

    # If we are only taking some columns, write the code to drop the ones we don't need!
    deleted_columns_one = set(step['dfs'][sheet_index_one].keys()).difference(set(selected_columns_one))
    deleted_columns_two = set(step['dfs'][sheet_index_two].keys()).difference(set(selected_columns_two))
    if len(deleted_columns_one) > 0:
        merge_code.append(
            f'{df_one_name}_tmp = {df_one_name}.drop({list(deleted_columns_one)}, axis=1)'
        )
    if len(deleted_columns_two) > 0:
        merge_code.append(
            f'{df_two_name}_tmp = temp_df.drop({list(deleted_columns_two)}, axis=1)'
        )

    # If we drop columns, we merge the new dataframes
    df_one_to_merge = df_one_name if len(deleted_columns_one) == 0 else f'{df_one_name}_tmp'
    df_two_to_merge = 'temp_df' if len(deleted_columns_two) == 0 else f'{df_two_name}_tmp'

    # We insist column names are unique in dataframes, so while we default the suffixes to be the dataframe
    # names
    suffix_one = df_one_name
    suffix_two = df_two_name if df_two_name != df_one_name else f'{df_two_name}_2'

    # Finially append the merge
    merge_code.append(
        f'{df_new_name} = {df_one_to_merge}.merge({df_two_to_merge}, left_on=[\'{merge_key_one}\'], right_on=[\'{merge_key_two}\'], how=\'left\', suffixes=[\'_{suffix_one}\', \'_{suffix_two}\'])'
    )

    # And then save it
    return merge_code


def describe_merge(
        sheet_index_one,
        merge_key_one, 
        selected_columns_one,
        sheet_index_two,
        merge_key_two,
        selected_columns_two,
        df_names=None
    ):

    if df_names is not None:
        df_one_name = df_names[sheet_index_one]
        df_two_name = df_names[sheet_index_two]
        return f'Merged {df_one_name} and {df_two_name}'
    return f'Merged dataframes {sheet_index_one} and {sheet_index_two}'


MERGE_STEP = {
    'step_version': 1,
    'step_display_name': MERGE_DISPLAY_NAME,
    'event_type': MERGE_EVENT,
    'step_type': MERGE_STEP_TYPE,
    'params': MERGE_PARAMS,
    'saturate': None,
    'execute': execute_merge_step,
    'transpile': transpile_merge_step,
    'describe': describe_merge
}