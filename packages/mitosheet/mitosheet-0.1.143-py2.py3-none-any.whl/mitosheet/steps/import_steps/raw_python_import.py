#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A raw python import, which allows you to import dataframes with the 
given Python code

NOTE: special care needs to be taken when upgrading this step, as it is used (e.g in the 
api in special ways). Not sure exactly how, but be careful + test it thoroughly.
"""
from mitosheet.utils import add_df_to_step, create_new_step, get_header_renames
from mitosheet.errors import make_df_exists_error
from mitosheet.mito_analytics import log
import json

RAW_PYTHON_IMPORT_DISPLAY_NAME = 'Imported Using Python Code'

RAW_PYTHON_IMPORT_EVENT = 'raw_python_import_edit'
RAW_PYTHON_IMPORT_STEP_TYPE = 'raw_python_import'

RAW_PYTHON_IMPORT_PARAMS = [
    'python_code', # a big string
    'new_df_names', # df names
]

def execute_raw_python_import(
        curr_step,
        python_code,
        new_df_names
    ):
    """
    Imports the python code - and makes sure to add the corresponding dataframes
    to the sheet itself
    """

    for df_name in new_df_names:
        if df_name in curr_step['df_names']:
            raise make_df_exists_error(df_name)

    # Create a new step
    new_step = create_new_step(curr_step, RAW_PYTHON_IMPORT_STEP_TYPE, deep=False)

    # Build a global string so these variables are defined in the outer scope (e.g. this executing code)
    global_string = ';'.join([f'global {df_name}' for df_name in new_df_names])
    # Actually run the code to define the variables
    exec(f'{global_string};{python_code}')
    # And then get the dataframes out of global storage (renaming any headers we need to along the way)
    column_header_renames = dict()
    for df_name in new_df_names:
        df = globals()[df_name]
        # If there are any invalid names, we perform a rename
        renames = get_header_renames(df.keys())
        if len(renames) > 0:
            # Save that we did these renames
            column_header_renames[df_name] = renames
            # Actually perform any renames we need to
            df.rename(columns=renames, inplace=True)

        add_df_to_step(new_step, df, df_name=df_name)
    
    # Save the renames that have occured in the step, for transpilation reasons
    new_step['column_header_renames'] = column_header_renames

    # Log that they used personal data.
    # Note: we assume that if they used a raw_python_import, then they used personal data 
    log('used_personal_data')

    return new_step


def transpile_raw_python_import(
        step,
        python_code,
        new_df_names
    ):
    """
    Transpiles a raw Python import to Python code. Because we're giving raw Python code,
    this is pretty easy - just split the code at the line breaks - and then
    perform any renames we need to.
    """
    code = python_code.split('\n')

    # Perform any renames we need to
    for df_name in step['column_header_renames']:
        renames = step['column_header_renames'][df_name]
        code.append(
            f'{df_name}.rename(columns={json.dumps(renames)}, inplace=True)'
        )

    return code


def describe_raw_python_import(
        python_code,
        new_df_names,
        df_names=None
    ):
    return f'Imported {", ".join(new_df_names)}'


RAW_PYTHON_IMPORT_STEP = {
    'step_version': 1,
    'step_display_name': RAW_PYTHON_IMPORT_DISPLAY_NAME,
    'event_type': RAW_PYTHON_IMPORT_EVENT,
    'step_type': RAW_PYTHON_IMPORT_STEP_TYPE,
    'params': RAW_PYTHON_IMPORT_PARAMS,
    'saturate': None,
    'execute': execute_raw_python_import,
    'transpile': transpile_raw_python_import,
    'describe': describe_raw_python_import
}