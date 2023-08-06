#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
After reading in the dataframe names from the frontend, 
sets their name in the widget state container
"""

from copy import deepcopy


DF_NAMES_UPDATE_EVENT = 'df_names_update'
DF_NAMES_UPDATE_PARAMS = ['df_names']

def execute_df_names_update(
        wsc,
        df_names
    ):
    """
    Changes the df_names in the current step - from information
    from the frontend
    """
    wsc.curr_step['df_names'] = deepcopy(df_names)


DF_NAMES_UPDATE = {
    'event_type': DF_NAMES_UPDATE_EVENT,
    'params': DF_NAMES_UPDATE_PARAMS,
    'execute': execute_df_names_update
}