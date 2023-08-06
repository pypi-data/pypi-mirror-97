#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions for saving and reading
in analyses.
"""

from mitosheet.upgrade import upgrade_saved_analysis_to_current_version
import os
import json

from mitosheet._version import __version__
from mitosheet.steps import STEPS
from mitosheet.profiling import timeit
from mitosheet.mito_analytics import log, get_dfs_metadata
from mitosheet.saves import SAVES


# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The current version of the saved Mito analysis
# where we save all the analyses for this version
SAVED_ANALYSIS_FOLDER = os.path.join(MITO_FOLDER, 'saved_analyses')


def read_analysis(analysis_name):
    """
    Given an analysis_name, reads the saved analysis in
    ~/.mito/{analysis_name}.json and returns a JSON object
    representing it.

    Also, checks if the analysis name is in the list of Mito
    saves, and will return that if so.
    """
    if analysis_name in SAVES:
        return SAVES[analysis_name]

    analysis_path = f'{SAVED_ANALYSIS_FOLDER}/{analysis_name}.json'

    if not os.path.exists(analysis_path):
        return None

    with open(analysis_path) as f:
        try:
            # We try and read the file as JSON
            return json.load(f)
        except: 
            return None

def read_and_upgrade_analysis(analysis_name):
    """
    Given an analysis_name, reads the saved analysis in
    ~/.mito/{analysis_name}.json, does it's best to upgrade it to the current
    saved version, and then returns it.
    """
    old_analysis = read_analysis(analysis_name)
    return upgrade_saved_analysis_to_current_version(old_analysis)

def _get_all_analysis_filenames():
    """
    Returns the names of the files in the SAVED_ANALYSIS_FOLDER
    """
    if not os.path.exists(SAVED_ANALYSIS_FOLDER):
        return []

    file_names = set([
        f for f in os.listdir(SAVED_ANALYSIS_FOLDER) 
        if os.path.isfile(os.path.join(SAVED_ANALYSIS_FOLDER, f))
    ])

    return file_names

def _delete_analyses(analysis_filenames):
    """
    For bulk deleting analysis with file names. 
    """
    for filename in analysis_filenames:
        os.remove(os.path.join(SAVED_ANALYSIS_FOLDER, filename))

def delete_saved_analysis(analysis_name):
    """
    Deletes a saved analysis. saved_analysis_file_name must end in .json

    Throws an error if analysis_name does not exist.
    """

    analysis = read_analysis(analysis_name)

    # If the saved_analysis_name exists, delete it
    if analysis is not None:
        os.remove(os.path.join(SAVED_ANALYSIS_FOLDER, analysis_name + '.json'))
    else:
        raise Exception(f'Cannot delete {analysis_name} as it does not exist')


def rename_saved_analysis(old_analysis_name, new_analysis_name):
    """
    Renames a saved analysis from old_analysis_name to new_analysis_name. 

    Throws an error if old_analysis_name does not exist, or new_analysis_name
    exists.
    """
    old_analysis = read_analysis(old_analysis_name)
    new_analysis = read_analysis(new_analysis_name)

    # If the old_analysis_file_name exists, and new_analysis_file_name does not exist
    if old_analysis is not None and new_analysis is None:
        full_old_analysis_name = os.path.join(SAVED_ANALYSIS_FOLDER, old_analysis_name + '.json')
        full_new_analysis_name = os.path.join(SAVED_ANALYSIS_FOLDER, new_analysis_name + '.json')
        os.rename(full_old_analysis_name, full_new_analysis_name)
    else:
        raise Exception(f'Invalid rename, with old and new analysis are {old_analysis_name} and {new_analysis_name}')


def read_saved_analysis_names():
    """
    Reads the names of all the analyses saved by the user.

    Does not return any of the auto-saved analyses!
    """
    if not os.path.exists(SAVED_ANALYSIS_FOLDER):
        return []

    file_names = [
        f for f in os.listdir(SAVED_ANALYSIS_FOLDER) 
        if os.path.isfile(os.path.join(SAVED_ANALYSIS_FOLDER, f))
        and not f.startswith('UUID-')
    ]

    # We make sure they are in alphabetical order!
    file_names.sort()

    return [
        file_name[:-5] for file_name in file_names 
        if file_name.endswith('.json')
    ]

@timeit
def saved_analysis_names_json():
    return json.dumps(read_saved_analysis_names())

def make_steps_json_obj(steps):
    """
    Given a steps dictonary from a widget_state_container, puts the steps
    into a format that can be saved and recreated. Necessary for saving an
    analysis to a file!
    """
    steps_json_obj = dict()
    for step_idx, step in enumerate(steps):
        step_type = step['step_type']
        
        for new_step in STEPS:
            if step_type == new_step['step_type']:

                # Save the step type
                step_summary = {
                    'step_version': new_step['step_version'],
                    'step_type': step_type,
                }
                # As well as all of the parameters for the step
                step_summary.update({key: value for key, value in step.items() if key in new_step['params']})

                steps_json_obj[step_idx] = step_summary

    return steps_json_obj

def write_saved_analysis(analysis_path, steps, version=__version__):
    with open(analysis_path, 'w+') as f:
        saved_analysis = {
            'version': version,
            'steps': steps
        }

        f.write(json.dumps(saved_analysis))

@timeit
def write_analysis(widget_state_container, analysis_name=None):
    """
    Writes the analysis saved in widget_state_container to
    ~/.mito/{analysis_name}. If analysis_name is none, gets the temporary
    name from the widget_state_container.

    NOTE: as the written analysis is from the widget_state_container,
    we assume that the analysis is valid when written and read back in!
    """

    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    if not os.path.exists(SAVED_ANALYSIS_FOLDER):
        os.mkdir(SAVED_ANALYSIS_FOLDER)

    if analysis_name is None:
        analysis_name = widget_state_container.analysis_name

    analysis_path = f'{SAVED_ANALYSIS_FOLDER}/{analysis_name}.json'
    steps = make_steps_json_obj(widget_state_container.steps)

    # Actually write the file
    write_saved_analysis(analysis_path, steps)

