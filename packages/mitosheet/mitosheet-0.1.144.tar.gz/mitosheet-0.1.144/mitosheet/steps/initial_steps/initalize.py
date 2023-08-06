#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
An initalize step, which is responsible for creating the _very first_
step in any mito analysis. It should transpile to nothing.
"""

from collections import OrderedDict
from mitosheet.utils import get_column_filter_type

INITIALIZE_DISPLAY_NAME = 'Created a Mitosheet'

INITIALIZE_EVENT = None
INITIALIZE_STEP_TYPE = 'initialize'

INITIALIZE_PARAMS = []

def execute_initialize_step(wsc, dfs):
    """
    The function responsible for updating the widget state container
    with a new initialize step.

    If it fails part of the way through, deletes the new initialize step entirely.
    """

    if len(wsc.steps) > 0:
        raise Exception("This step should only be applied at the start of an analysis")
    
    # NOTE: changing this variable is a hefty task - as you need to update all the steps
    # that modify these variables. Take care!
    wsc.steps = [{
        'step_id': 'init',
        'step_type': INITIALIZE_STEP_TYPE, # the first step is a unique step type that is just the first step!
        # The column_metatype is if it stores formulas or values
        'column_metatype': [{key: 'value' for key in df.keys()} for df in dfs], 
        # The column_type is the type of the series in this column 
        'column_type': [{key: get_column_filter_type(df[key]) for key in df.keys()} for df in dfs],
        # We make column_spreadsheet_code an ordered dictonary to preserve the order the formulas
        # are inserted, which in turn makes sure when we save + rerun an analysis, it's recreated
        # in the correct order (and thus the column order is preserved).
        'column_spreadsheet_code': [OrderedDict({key: '' for key in df.keys()}) for df in dfs],
        # We also keep track of a list of the added columns in this step, so we can make
        # sure columns get defined in the correct order in the transpiled code
        'added_columns': [[] for df in dfs],
        'column_python_code': [{key: '' for key in df.keys()} for df in dfs],
        'column_evaluation_graph': [{key: set() for key in df.keys()} for df in dfs],
        'column_filters': [{key: {'operator': 'And', 'filters': []} for key in df.keys()} for df in dfs],
        'dfs': dfs,
        # The df_names are composed of two parts:
        # 1. The names of the variables passed into the mitosheet.sheet call (which don't change over time).
        # 2. The names of the dataframes that were created during the analysis (e.g. by a merge).
        # Until we get them from the frontend as an update_event, we default them to df1, df2, ...
        'df_names': [f'df{i + 1}' for i in range(len(dfs))] 
    }]


def transpile_initialize_step(widget_state_container, step):
    """
    Transpiles a initialize step to python code!
    """
    return []

def describe_initialize_step(df_names=None):
    if df_names is not None: 
        imported_df_names = ', '.join([df_name for df_name in df_names])
        return f'Created a mitosheet with {imported_df_names} dataframes'
    return f'Created a mitosheet'

"""
This object wraps all the information
that is needed for a initialize step!
"""
INITIALIZE_STEP = {
    'event_type': INITIALIZE_EVENT,
    'step_display_name': INITIALIZE_DISPLAY_NAME,
    'step_type': INITIALIZE_STEP_TYPE,
    'params': INITIALIZE_PARAMS,
    'saturate': None,
    'execute': execute_initialize_step,
    'transpile': transpile_initialize_step,
    'describe': describe_initialize_step
}





