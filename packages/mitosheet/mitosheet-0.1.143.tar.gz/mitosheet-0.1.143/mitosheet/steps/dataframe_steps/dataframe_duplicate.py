#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
This steps duplicates a dataframe of a given index. 
"""

from mitosheet.utils import add_df_to_step, create_new_step


DATAFRAME_DUPLICATE_DISPLAY_NAME = 'Duplicated a Dataframe'

DATAFRAME_DUPLICATE_EVENT = 'dataframe_duplicate_edit'
DATAFRAME_DUPLICATE_STEP_TYPE = 'dataframe_duplicate'

DATAFRAME_DUPLICATE_PARAMS = [
    'sheet_index'
]

def get_first_unused_name(df_names, dataframe_name):
    """
    Appends _1, _2, .. to df name until it finds an unused 
    dataframe name. If no append is necessary, will just return
    """
    if dataframe_name not in df_names:
        return dataframe_name

    for i in range(len(df_names) + 1):
        new_name = f'{dataframe_name}_{i + 1}'
        if new_name not in df_names:
            return new_name


def execute_dataframe_duplicate(
        curr_step,
        sheet_index
    ):
    """
    Duplicates the dataframe at sheet_index.
    """
    # Create a new step and save the parameters
    new_step = create_new_step(curr_step, DATAFRAME_DUPLICATE_STEP_TYPE, deep=False)

    # Save the parameters
    new_step['sheet_index'] = sheet_index

    # Execute the step
    df_copy = new_step['dfs'][sheet_index].copy(deep=True)
    new_name = get_first_unused_name(new_step['df_names'], new_step['df_names'][sheet_index] + '_copy')
    add_df_to_step(new_step, df_copy, new_name)

    return new_step


def transpile_dataframe_duplicate(
        step,
        sheet_index
    ):
    """
    Transpiles the dataframe duplication to Python code
    """
    old_df_name = step['df_names'][sheet_index]
    new_df_name = step['df_names'][len(step['dfs']) - 1]

    return [f'{new_df_name} = {old_df_name}.copy(deep=True)']


def describe_dataframe_duplicate(
        sheet_index,
        df_names=None
    ):

    if df_names is not None:
        old_df_name = df_names[sheet_index]
        new_df_name = df_names[len(df_names) - 1]
        return f'Duplicated {old_df_name} to {new_df_name}'
    return f'Duplicated a df'


DATAFRAME_DUPLICATE_STEP = {
    'step_version': 1,
    'step_display_name': DATAFRAME_DUPLICATE_DISPLAY_NAME,
    'event_type': DATAFRAME_DUPLICATE_EVENT,
    'step_type': DATAFRAME_DUPLICATE_STEP_TYPE,
    'params': DATAFRAME_DUPLICATE_PARAMS,
    'saturate': None,
    'execute': execute_dataframe_duplicate,
    'transpile': transpile_dataframe_duplicate,
    'describe': describe_dataframe_duplicate
}