#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Deletes a dataframe from everywhere in the step.
"""

from mitosheet.utils import create_new_step


DATAFRAME_DELETE_DISPLAY_NAME = 'Deleted a Dataframe'

DATAFRAME_DELETE_EVENT = 'dataframe_delete_edit'
DATAFRAME_DELETE_STEP_TYPE = 'dataframe_delete'

DATAFRAME_DELETE_PARAMS = [
    'sheet_index',
    'old_dataframe_name'
]

def saturate_dataframe_delete(
        wsc,
        event
    ):
    """
    Adds the old dataframe name to the dataframe_delete event
    """
    sheet_index = event['sheet_index']
    old_dataframe_name = wsc.curr_step['df_names'][sheet_index]
    event['old_dataframe_name'] = old_dataframe_name


def execute_dataframe_delete(
        curr_step,
        sheet_index,
        old_dataframe_name
    ):
    """
    Deletes the dataframe as sheet index.
    """
    # Create a new step and save the parameters
    new_step = create_new_step(curr_step, DATAFRAME_DELETE_STEP_TYPE, deep=False)

    # Save the parameters
    new_step['sheet_index'] = sheet_index
    new_step['old_dataframe_name'] = old_dataframe_name

    # Execute the delete
    new_step['column_metatype'].pop(sheet_index)
    new_step['column_type'].pop(sheet_index)
    new_step['column_spreadsheet_code'].pop(sheet_index)
    new_step['added_columns'].pop(sheet_index)
    new_step['column_python_code'].pop(sheet_index)
    new_step['column_evaluation_graph'].pop(sheet_index)
    new_step['column_filters'].pop(sheet_index)
    new_step['dfs'].pop(sheet_index)
    new_step['df_names'].pop(sheet_index)

    return new_step

def transpile_dataframe_delete(
        step,
        sheet_index,
        old_dataframe_name
    ):
    """
    Transpiles a delete step (which doesn't do much, in fairness).
    """
    return [f'del {old_dataframe_name}']


def describe_dataframe_delete(
        sheet_index,
        old_dataframe_name,
        df_names=None
    ):
    return f'Deleted dataframe {old_dataframe_name}'


DATAFRAME_DELETE_STEP = {
    'step_version': 1,
    'step_display_name': DATAFRAME_DELETE_DISPLAY_NAME,
    'event_type': DATAFRAME_DELETE_EVENT,
    'step_type': DATAFRAME_DELETE_STEP_TYPE,
    'params': DATAFRAME_DELETE_PARAMS,
    'saturate': saturate_dataframe_delete,
    'execute': execute_dataframe_delete,
    'transpile': transpile_dataframe_delete,
    'describe': describe_dataframe_delete
}