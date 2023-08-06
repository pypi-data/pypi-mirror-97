#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Our general approach to logging can be understood as:
0. Users are identified by a single random ID that we generate on the client-side, 
   here. We store this in the ~/.mito/user.json file, and we use it as the permanent
   ID for all users.
1. All logging is on the backend. This avoids us worrying about blockers or needing
   to associate with ad-tech at all.
2. We generate a single log event for a single action taken by the user. That means that if
   the user takes an action that causes an error, the error is logged _with_ that action.

   This appears to be good practice, as it allows us to associate what actions are taken
   with their result very effectively!
3. Log as little as is necessary. A messy log makes it very hard to see what's important
   so we default to not logging enough rather than logging to much. It's easy to add on
   logging, but harder to remove code.
"""
from typing import List

import analytics
# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 

import pandas as pd
import sys
import getpass
import json

from mitosheet.user.user_utils import get_user_field
from mitosheet._version import __version__
from mitosheet.errors import get_recent_traceback_as_list
import platform # Package for getting the operating system of the user

def identify():
    """
    Helper function for identifying a user to Segment
    """
    static_user_id = get_user_field('static_user_id')
    user_email = get_user_field('user_email')

    # Get the operating system
    operating_system = platform.system()

    analytics.identify(static_user_id, {
        'location': __file__,
        'python_version': sys.version_info,
        'mito_version': __version__,
        'operating_system': operating_system,
        'email': user_email,
        'user': getpass.getuser(),
    })

def log(log_event, params=None):
    if params is None:
        params = {}

    analytics.track(
        get_user_field('static_user_id'), 
        log_event, 
        params
    )


def log_recent_error(log_event=None):
    """
    A helper function for logging the most recent error that has occured.

    log_event defaults to an execution_error_log_event
    """
    if log_event is None:
        log_event = 'execution_error_log_event'

    # We get the error, see more here: https://wiki.python.org/moin/HandlingExceptions
    e = sys.exc_info()[0]

    # If we have some other error, we just report this as an execution error
    log(
        log_event, 
        {
            'header': 'Execution Error', 
            'to_fix': 'Sorry, there was an error during executing this code.',
            'error': str(e),
            'traceback': get_recent_traceback_as_list()
        }
    )



def log_event_processed(event, widget_state_container, failed=False, edit_error=None):
    """
    Helper function for logging when an event is processed
    by the widget state container. 

    Does it's best to fill in helpful meta-data for interpreting the event
    including the state of the widget_state_container _after_ the step
    was applied.

    NOTE: if processing the event fails, then failed should be True. If there was an
    edit error that was thrown during the processing of the event, then edit_error
    should be set to that error.
    """
    try:
        # First, we get all the params of the event, and append them with _params_
        event_properties = {
            'params_' + key: value for key, value in event.items()
        }

        # If it's an import event, we also log the dataframe metadata
        # (and we also log in the case of a replayed analysis)
        if 'import' in event['type'] or 'replay_analysis_update' in event['type']:
            df_properties = get_dfs_metadata(widget_state_container.dfs)
        else:
            df_properties = {}

        # We also get some metadata about the widget state container at this state
        wsc_properties = {
            # NOTE: analysis name is the UUID that mito saves the analysis under
            'wsc_analysis_name': widget_state_container.analysis_name,
            'wsc_curr_step_idx': widget_state_container.curr_step_idx,
            'wsc_curr_step_type': widget_state_container.curr_step['step_type'],
            'wsc_df_names': widget_state_container.curr_step['df_names']
        }

        # Python properties, just for helpful data about the system
        python_properties = {
            'version_python': sys.version_info,
            'version_mito': __version__ 
        }

        # We also check there is an edit_error, and if there is, then we add the error logs
        if edit_error is not None:
            error_properties = {
                'error_type': edit_error.type_,
                'error_header': edit_error.header,
                'error_to_fix': edit_error.to_fix,
                'error_traceback': get_recent_traceback_as_list(),
            }
        elif failed:
            # Otherwise, if there is no edit_error, and we still failed, then we must have
            # gotten an execution error
            error_properties = {
                'error_type': 'execution_error',
                'error_header': 'Execution Error',
                'error_traceback': get_recent_traceback_as_list(),
            }
        else:
            error_properties = {}

        # We choose to log the event type, as it is the best high-level item for our logs
        # and we append a _failed if the event failed in doing this.
        log_event = event['type'] + ('_failed' if failed else '')

        log(
            log_event, 
            dict(
                **python_properties,
                **event_properties,
                **wsc_properties,
                **df_properties,
                **error_properties
            )
        )
    except:
        # We don't want logging to ever brick the application, so if the logging fails
        # we just log simple information about the event. This should never occur, but it
        # is just a precaution - some defensive programming so to speak
        log(
            event['type'],
            event
        )

def get_dfs_metadata(dfs: List[pd.DataFrame]):
    """
    A helper function to log metadata about a list of dataframes, 
    that does not pass any sensitive information of the dataframe
    elsewhere.
    """
    try:
        df_shapes = {f'df_{idx}_shape': {'row': df.shape[0], 'col': df.shape[1]} for idx, df in enumerate(dfs)}
        df_headers = {f'df_{idx}_headers': list(df.keys()) for idx, df in enumerate(dfs)}
        df_dtypes = {f'df_{idx}_dtypes': [str(df[key].dtype) for key in df.keys()] for idx, df in enumerate(dfs)}

        return dict(
            {'df_count': len(dfs)},
            **df_shapes,
            **df_headers,
            **df_dtypes
        )
    except:
        # We don't mind if logging fails
        pass
    return {}
