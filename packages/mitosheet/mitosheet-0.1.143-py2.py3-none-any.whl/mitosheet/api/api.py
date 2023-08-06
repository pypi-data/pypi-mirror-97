#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains handlers for the Mito API
"""
import os
import json
from pathlib import Path
import pandas as pd

from mitosheet.api.get_column_dtype import get_column_dtype
from mitosheet.api.get_column_summary_graph import get_column_summary_graph
from mitosheet.api.get_saved_analysis_description import get_saved_analysis_description
from mitosheet.steps.import_steps.raw_python_import import RAW_PYTHON_IMPORT_STEP_TYPE
from mitosheet.steps.import_steps.simple_import import SIMPLE_IMPORT_STEP_TYPE
from mitosheet.save_utils import read_analysis
from mitosheet.mito_analytics import log

def get_filenames_with_suffix(suffix):
    """
    Returns all the file names in the current folder that end with the given
    suffix, sorted from most-recently created to the oldest.
    """
    # We sort them by creation time, to get the most recent files, as the user
    # is more likely to want these
    filenames = sorted(Path('.').iterdir(), key=os.path.getmtime)
    filenames.reverse()
    return [str(filename) for filename in filenames if filename.suffix == suffix]


def handle_datafiles(send, event):
    """
    Handles a `datafiles` api call, and returns all the csv files
    in the current folder.
    """
    csv_files = get_filenames_with_suffix('.csv')
    # TODO: also get the XLSX files, when we can import them
    send({
        'event': 'api_response',
        'id': event['id'],
        'data': csv_files
    })

def handle_import_summary(send, event):
    """
    Handle import summary is a route that, given the name of an analysis, will
    return the parameters to import steps over the course of the analysis. 

    The data we return is in the format:
    {
        "1": {
            "file_names": ["file123.csv"]
        }, 
        "3": {
            "python_code": "import pandas as ...",
            "new_df_names": ["df1"]
        }
    }
    which is a mapping from raw import steps to the files that they import.
    """
    analysis_name = event['analysis_name']
    # NOTE: we don't upgrade, as this happens when you actually choose to replay an analysis
    analysis = read_analysis(analysis_name)

    imports_only = dict()
    if analysis is not None:
        for step_idx, step in analysis['steps'].items():
            if step['step_type'] == SIMPLE_IMPORT_STEP_TYPE:
                imports_only[step_idx] = dict()
                imports_only[step_idx]['step_type'] = SIMPLE_IMPORT_STEP_TYPE
                imports_only[step_idx]['file_names'] = step['file_names']
            elif step['step_type'] == RAW_PYTHON_IMPORT_STEP_TYPE:
                imports_only[step_idx] = dict()
                imports_only[step_idx]['step_type'] = RAW_PYTHON_IMPORT_STEP_TYPE
                imports_only[step_idx]['python_code'] = step['python_code']
                imports_only[step_idx]['new_df_names'] = step['new_df_names']

    send({
        'event': 'api_response',
        'id': event['id'],
        'data': imports_only
    })

def get_dataframe_as_csv(send, event, wsc):
    """
    Sends a dataframe as a CSV string
    """
    sheet_index = event['sheet_index']
    df = wsc.dfs[sheet_index]

    send({
        'event': 'api_response',
        'id': event['id'],
        'data': df.to_csv(index=False)
    })


def get_column_describe(send, event, wsc):
    """
    Sends back a string that can be parsed to a JSON object that
    contains _all_ the results from the series .describe function
    for the series at column_header in the df at sheet_index.
    """
    sheet_index = event['sheet_index']
    column_header = event['column_header']
    
    series: pd.Series = wsc.dfs[sheet_index][column_header]
    describe = series.describe()

    try:
        describe_obj = {}
        describe_obj['count NaN'] = str(series.isna().sum())
        for index, row in describe.iteritems():
            # We turn all the items to strings, as some items are not valid JSON
            # e.g. some wacky numpy datatypes. This allows us to send all of this 
            # to the front-end
            describe_obj[index] = str(row)

        send({
            'event': 'api_response',
            'id': event['id'],
            'data': json.dumps(describe_obj)
        })
    except:
        # As this is also a non-critical error, we don't want to display an error
        # message in the case of failure, so we just return nothing
        send({
            'event': 'api_response',
            'id': event['id'],
            'data': ''
        })



def handle_api_event(send, event, wsc):
    """
    Handler for all API calls. Note that any response to the
    API must return the same ID that the incoming message contains,
    so that the frontend knows how to match the responses.
    """    
    # And then handle it
    if event['type'] == 'datafiles':
        handle_datafiles(send, event)
    elif event['type'] == 'import_summary':
        handle_import_summary(send, event)
    elif event['type'] == 'get_dataframe_as_csv':
        get_dataframe_as_csv(send, event, wsc)
    elif event['type'] == 'get_column_summary_graph':
        get_column_summary_graph(send, event, wsc)
    elif event['type'] == 'get_column_describe':
        get_column_describe(send, event, wsc)
    elif event['type'] == 'get_column_dtype':
        get_column_dtype(send, event, wsc)
    elif event['type'] == 'get_saved_analysis_description':
        get_saved_analysis_description(send, event, wsc)
    else:
        raise Exception(f'Event: {event} is not a valid API call')