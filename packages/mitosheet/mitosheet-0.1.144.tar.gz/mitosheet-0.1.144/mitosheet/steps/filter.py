#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A filter steps, which allows you to filter a column based on some
conditions and some values. 

NOTE: there are some workarounds in this step with old filter steps being deleted
and remade (like the one right) - simply because we don't have a way of editing
old steps otherwise!
"""
import functools
from mitosheet.utils import create_new_step, does_sheet_index_exist_within_step
from numbers import Number
import pandas as pd
from datetime import date

from mitosheet.errors import (
    EditError,
    make_execution_error,
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_filter_error
)

FILTER_COLUMN_DISPLAY_NAME = 'Filtered a Column'

FILTER_COLUMN_EVENT = 'filter_column_edit'
FILTER_COLUMN_STEP_TYPE = 'filter_column'

FILTER_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # column to filter from
    'operator', # 'Or' or 'And'
    # Filters are either a tripples of ({'type': <type>, 'condition': <condition>, 'value': <value>}),
    # or they are objects with {'filters': [list of above tripples], 'operator': 'Or' or 'And'}
    'filters', 
]


# CONSTANTS USED IN THE FILTER STEP ITSELF

STRING_TYPE = 'string'
NUMBER_TYPE = 'number'
DATETIME_TYPE = 'datetime'

SHARED_FILTER_CONDITIONS = [
    'empty',
    'not_empty'
]

STRING_FILTER_CONDITIONS = [
    'contains',
    'string_does_not_contain',
    'string_exactly'
]

NUMBER_FILTER_CONDITIONS = [
    'number_exactly',
    'greater',
    'greater_than_or_equal',
    'less',
    'less_than_or_equal'
]

DATETIME_FILTER_CONDITIONS = [
    'datetime_exactly',
    'datetime_greater',
    'datetime_greater_than_or_equal',
    'datetime_less',
    'datetime_less_than_or_equal',
]


def execute_filter_column(
        wsc,
        sheet_index,
        column_header,
        operator,
        filters
    ):
    """
    Filters an existing sheet with the given filters, which 
    each contain a condition and an optional value.
    """
    last_step = wsc.steps[-1]

    # if the sheet doesn't exist, throw an error
    if not does_sheet_index_exist_within_step(last_step, sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the filtered column exists 
    missing_column = set([column_header]).difference(last_step['column_metatype'][sheet_index].keys())
    if len(missing_column) > 0: 
        raise make_no_column_error(missing_column)

    # if there is a filter already applied to the column, remove it
    _reset_filter(wsc, sheet_index, column_header)

    # if the condition is none, don't create a new step and delete the current filter if it exists
    if len(filters) == 0:
        # if there is a filter already applied to the column, remove it
        return

    last_step = wsc.steps[-1]


    # If no errors we create a new step for this filter
    new_step = create_new_step(last_step, FILTER_COLUMN_STEP_TYPE)
    # NOTE: we actually have to save these parameters in the step, as the filter step acts
    # differently than all other steps, tragically
    new_step['sheet_index'] = sheet_index
    new_step['column_header'] = column_header
    new_step['filters'] = filters
    new_step['operator'] = operator

    # Then we update the dataframe, first by executing on a fake dataframe
    try:
        # TODO: Remove this speculative execution, when it's safe to do so
        # (e.g. when we have proper step editing). 
        # For now, because filter is wacky, we leave it in here... 

        # make a copy of our data frame to test operate on 
        df_copy = new_step['dfs'][sheet_index].copy(deep=True)

        # We execute on the copy first to see if there will be errors
        _execute_filter(
            df_copy, 
            column_header,
            operator,
            filters
        )

    except EditError as e:
        # We propagate this error upwards
        raise e
    except Exception as e:
        print(e)
        # We raise a generic execution error in this case!
        raise make_execution_error()


    # if there was no error in execution on the copy, execute on real dataframes
    new_step['dfs'][sheet_index] = _execute_filter(
        new_step['dfs'][sheet_index], 
        column_header,
        operator,
        filters
    )

    # keep track of which columns are filtered
    new_step['column_filters'][sheet_index][column_header]['operator'] = operator
    new_step['column_filters'][sheet_index][column_header]['filters'] = filters

    wsc.steps.append(new_step)
    wsc.curr_step_idx = len(wsc.steps) - 1


def _reset_filter(wsc, sheet_index, column_header, ignore_last_step=False):
    """
    To reset the filter, we:

    1. Delete the filter step.
    2. Save the analysis.
    3. Delete _all_ the steps (ik, crazy).
    4. Replay the analysis.

    NOTE: we do this as a workaround because we want users to be able to edit
    filters, but there is currently no way to go back to a step and edit it. 

    We should _heavily_ re-evaluate this screwy-ness when we allow editing of steps, 
    and rolling back to steps.
    """
    # NOTE: we import here to avoid circular imports. This is an unfortunate
    # side effect of this entire workaround :( )
    from mitosheet.updates.replay_analysis import execute_replay_analysis_update
    from mitosheet.save_utils import write_analysis

    deleted_step_idx = None

    # find the step to delete
    for step_idx, step in enumerate(wsc.steps):
        if ignore_last_step and step_idx == wsc.curr_step_idx:
            continue

        if step['step_type'] == FILTER_COLUMN_STEP_TYPE:
            # If this is the step that added a filter to the column, mark it as the one to delete
            if step['sheet_index'] == sheet_index and step['column_header'] == column_header:
                deleted_step_idx = step_idx

    # if there are no step to delete, return
    if deleted_step_idx == None:
        return
    
    # Delete the filter step
    wsc.steps.pop(deleted_step_idx)

    # save the current analysis, now without the filter step
    write_analysis(wsc)

    # Delete _all the steps_ except the first
    wsc.steps = [wsc.steps[0]]

    # Rerun the analysis
    execute_replay_analysis_update(wsc, wsc.analysis_name, None, False)


def get_applied_filter(df, column_header, filter_):
    """
    Given a filter triple, returns the filter indexes for that
    actual dataframe
    """
    type_ = filter_['type']
    condition = filter_['condition']
    value = filter_['value']

    # First, we case on the shared conditions, to get them out of the way
    if condition in SHARED_FILTER_CONDITIONS:
        if condition == 'empty':
            return df[column_header].isna()
        elif condition == 'not_empty':
            return df[column_header].notnull()

    if type_ == STRING_TYPE:
        if condition not in STRING_FILTER_CONDITIONS:
            raise Exception(f'Invalid condition passed to string filter {condition}')

        # Check that the value is the valid
        if not isinstance(value, str):
            raise make_invalid_filter_error(value, STRING_TYPE)

        if condition == 'contains':
            return df[column_header].str.contains(value, na=False)
        if condition == 'string_does_not_contain':
            return ~df[column_header].str.contains(value, na=False)
        elif condition == 'string_exactly':
            return df[column_header] == value

    elif type_ == NUMBER_TYPE:
        if condition not in NUMBER_FILTER_CONDITIONS:
            raise Exception(f'Invalid condition passed to number filter {condition}')
        
        # Check that the value is the valid
        if not isinstance(value, Number):
            raise make_invalid_filter_error(value, NUMBER_TYPE)

        if condition == 'number_exactly':
            return df[column_header] == value
        elif condition == 'greater':
            return df[column_header] > value
        elif condition == 'greater_than_or_equal':
            return df[column_header] >= value
        elif condition == 'less':
            return df[column_header] < value
        elif condition == 'less_than_or_equal':
            return df[column_header] <= value

    elif type_ == DATETIME_TYPE:
        if condition not in DATETIME_FILTER_CONDITIONS:
            raise Exception(f'Invalid condition passed to datetime filter {condition}')

        # Check that we were given something that can be understood as a date
        try:
            timestamp = pd.to_datetime(value)
        except:
            # If we hit an error, because we restrict the input datetime, 
            # this is probably occuring because the user has only partially input the date, 
            # and so in this case, we just default it to the minimum possible timestamp for now!
            timestamp = date.min

        if condition == 'datetime_exactly':
            return df[column_header] == timestamp
        elif condition == 'datetime_greater':
            return df[column_header] > timestamp
        elif condition == 'datetime_greater_than_or_equal':
            return df[column_header] >= timestamp
        elif condition == 'datetime_less':
            return df[column_header] < timestamp
        elif condition == 'datetime_less_than_or_equal':
            return df[column_header] <= timestamp
    else:
        raise Exception(f'Invalid type passed in filter {type_}')

def combine_filters(operator, filters):

    def filter_reducer(filter_one, filter_two):
        # helper for combining filters based on the operations
        if operator == 'Or':
            return (filter_one) | (filter_two)
        elif operator == 'And':
            return (filter_one) & (filter_two)
        else:
            raise Exception(f'Operator {operator} is unsupported')

    # Combine all the filters into a single filter
    return functools.reduce(filter_reducer, filters)

def _execute_filter(
        df, 
        column_header,
        operator,
        filters
    ):
    """
    Executes a filter on the given column, filtering by removing any rows who
    don't meet the condition.
    """

    applied_filters = []

    for filter_or_group in filters:

        # If it's a group, then we build the filters for the group, combine them
        # and then add that to the applied filters
        if 'filters' in filter_or_group:
            group_filters = []
            for filter_ in filter_or_group['filters']:
                group_filters.append(
                    get_applied_filter(df, column_header, filter_)
                )

            applied_filters.append(
                combine_filters(filter_or_group['operator'], group_filters)
            )    

        # Otherwise, we just get that specific filter, and append it
        else:
            applied_filters.append(get_applied_filter(df, column_header, filter_or_group))    
    
    return df[combine_filters(operator, applied_filters)].reset_index(drop=True)


def get_filter_string(df_name, column_header, filter_):
    """
    Transpiles a specific filter to a fitler string, to be used
    in constructing the final transpiled code
    """
    condition = filter_['condition']
    value = filter_['value']

    FILTER_FORMAT_STRING_DICT = {
        # SHARED CONDITIONS
        'empty': '{df_name}.{column_header}.isna()',
        'not_empty': '{df_name}.{column_header}.notnull()',

        # NUMBERS
        'number_exactly': '{df_name}[\'{column_header}\'] == {value}',
        'greater': '{df_name}[\'{column_header}\'] > {value}',
        'greater_than_or_equal': '{df_name}[\'{column_header}\'] >= {value}',
        'less': '{df_name}[\'{column_header}\'] < {value}',
        'less_than_or_equal': '{df_name}[\'{column_header}\'] <= {value}',
        
        # STRINGS
        'contains': '{df_name}[\'{column_header}\'].str.contains(\'{value}\', na=False)',
        'string_does_not_contain': '~{df_name}[\'{column_header}\'].str.contains(\'{value}\', na=False)',
        'string_exactly': '{df_name}[\'{column_header}\'] == \'{value}\'',

        # DATES
        'datetime_exactly': '{df_name}[\'{column_header}\'] == pd.to_datetime(\'{value}\')',
        'datetime_greater': '{df_name}[\'{column_header}\'] > pd.to_datetime(\'{value}\')',
        'datetime_greater_than_or_equal': '{df_name}[\'{column_header}\'] >= pd.to_datetime(\'{value}\')',
        'datetime_less': '{df_name}[\'{column_header}\'] < pd.to_datetime(\'{value}\')',
        'datetime_less_than_or_equal': '{df_name}[\'{column_header}\'] <= pd.to_datetime(\'{value}\')',            
    }

    return FILTER_FORMAT_STRING_DICT[condition].format(
        df_name=df_name,
        column_header=column_header,
        value=value
    )

def combine_filter_strings(operator, filter_strings, split_lines=False):
    """
    Combines the given filter strings with the passed operator, optionally 
    splitting the lines at 120 characters.
    
    NOTE: we choose to keep groups together for readibility, and so do not
    split the lines if we are combing a group.
    """
    if len(filter_strings) == 1:
        return filter_strings[0]
    else:
        # If there are multiple conditions, we combine them together, with the
        # given operator in the middle
        OPERATOR_SIGNS = {
            'Or': '|',
            'And': '&'
        }
        # Put parens around them
        filter_strings = [
            f'({fs})' for fs in filter_strings
        ]

        filter_string = ''
        current_line_length = 0
        for i, fs in enumerate(filter_strings):
            if i != 0:
                filter_string += f' {OPERATOR_SIGNS[operator]} '
            filter_string += fs
            # We keep track of how long the lines are, and if they go over 100 characters,
            # then we split them into a new line (not if this is the last one though)
            current_line_length += len(fs)
            if split_lines and current_line_length > 100 and i != len(filter_strings) - 1:
                filter_string += ' \\\n\t'
                current_line_length = 0

        return filter_string


def transpile_filter_column(
        step,
        sheet_index,
        column_header,
        operator,
        filters
    ):
    """
    Transpiles a filter step to Python code. 
    """
    df_name = step['df_names'][sheet_index]

    filter_strings = []
    for filter_or_group in filters:
        # If it is a group, we build the code for each filter, and then combine them at the end
        if 'filters' in filter_or_group:
            group_filter_strings = []
            for filter_ in filter_or_group['filters']:
                group_filter_strings.append(
                    get_filter_string(df_name, column_header, filter_)
                )

            filter_strings.append(
                # Note: we add parens around this, so it's grouped properly
                "(" + combine_filter_strings(filter_or_group['operator'], group_filter_strings) + ")"
            )
        else:
            filter_strings.append(
                get_filter_string(df_name, column_header, filter_or_group)
            )

    if len(filter_strings) == 0:
        return []
    elif len(filter_strings) == 1:
        return [
            f'{df_name} = {df_name}[{filter_strings[0]}]',
            f'{df_name} = {df_name}.reset_index(drop=True)'
        ]
    else:
        filter_string = combine_filter_strings(operator, filter_strings, split_lines=True)
        return [
            f'{df_name} = {df_name}[{filter_string}]',
            f'{df_name} = {df_name}.reset_index(drop=True)'
        ]


def describe_filter_column(
        sheet_index,
        column_header,
        operator,
        filters,
        df_names=None
    ):

    if df_names is not None:
        df_name = df_names[sheet_index]
        return f'Filtered {column_header} in {df_name}'
    return f'Filtered {column_header}'


FILTER_STEP = {
    'step_version': 1,
    'step_display_name': FILTER_COLUMN_DISPLAY_NAME,
    'event_type': FILTER_COLUMN_EVENT,
    'step_type': FILTER_COLUMN_STEP_TYPE,
    'params': FILTER_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_filter_column,
    'transpile': transpile_filter_column,
    'describe': describe_filter_column
}