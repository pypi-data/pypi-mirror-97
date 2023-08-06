#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains functions for upgrading analyses!

NOTE: when adding a specific function for upgrading one version of a step to the other, the
format of the function should be:

def upgrade_<old_step_type>_<old_step_version>_to_<new_step_type>_<new_step_version>(step):
    ....
"""

from mitosheet._version import __version__


def ugprade_group_1_to_pivot_2(step):
    """
    Upgrades from a group 1 step to a pivot 2 step, simply
    by changing the names of the params.

    Old format of the step: {
        "step_version": 1, 
        "step_type": "group", 
        "sheet_index": x, 
        "group_rows": [...], 
        "group_columns": [...], 
        "values": {...: ...}}}
    }

    New format of the step: {
        "step_version": 2, 
        "step_type": "pivot", 
        "sheet_index": old['sheet_index'], 
        "pivot_rows": old['group_rows'], 
        "pivot_columns": old['group_columns'], 
        "values": old['values']
    }
    """
    return {
        'step_version': 2,
        'step_type': 'pivot',
        'sheet_index': step['sheet_index'],
        'pivot_rows': step['group_rows'],
        'pivot_columns': step['group_columns'],
        'values': step['values']
    }

"""
STEP_UPGRADES_FUNCTION_MAPPING mapping contains a mapping of all steps that need to be upgraded. A step
x at version y needs to be upgraded if STEP_UPGRADES[x][y] is defined, and in fact 
this mapping contains the function that can be used to do the upgrade!
 
NOTE: upgrades of steps should form a linear graph of upgrades to the most up to date
version. For example, if we change add_column from version 1 to version 2 to version 3, 
this object should contain:
    {
        'add_column': {
            1: ugprade_add_column_1_to_add_column_2,
            2: ugprade_add_column_2_to_add_column_3
        }
    }
"""
STEP_UPGRADES_FUNCTION_MAPPING = {
    'group': {
        1: ugprade_group_1_to_pivot_2
    }
}


def is_prev_version(version: str, curr_version: str=__version__):
    """
    Returns True if the passed version is a previous version compared
    to the current version; note that this assumes semantic versioning
    with x.y.z!
    """
    old_version_parts = version.split('.')
    curr_version_parts = curr_version.split('.')

    for old_version_part, curr_version_part in zip(old_version_parts, curr_version_parts):
        if int(old_version_part) > int(curr_version_part):
            # E.g. if we have 0.2.11 and 0.1.11, we want to return early as it's clearly not older!
            return False

        if int(old_version_part) < int(curr_version_part):
            return True

    return False

def needs_upgrade(steps):
    """
    Returns True if _any_ of the steps in this step dictonary
    needs to be upgraded!
    """
    for step_idx, step in steps.items():
        step_version = step['step_version']
        step_type = step['step_type']

        if step_type in STEP_UPGRADES_FUNCTION_MAPPING:
            step_upgrades = STEP_UPGRADES_FUNCTION_MAPPING[step_type]
            if step_version in step_upgrades:
                return True

    return False


def upgrade_saved_analysis_to_current_version(saved_analysis):
    """
    Upgrades a saved analysis to the current version!
    """
    if saved_analysis is None:
        return None

    version = saved_analysis['version']
    steps = saved_analysis['steps']

    if not is_prev_version(version) or not needs_upgrade(steps):
        # TODO: do we want to _change_ the version this was saved with? I think it doesn't
        # really matter, as it gets changed when it gets rewritten...
        return saved_analysis

    new_steps = []
    for step_idx, step in steps.items():
        step_version = step['step_version']
        step_type = step['step_type']
        new_step = step

        if step_type in STEP_UPGRADES_FUNCTION_MAPPING:
            step_upgrades = STEP_UPGRADES_FUNCTION_MAPPING[step_type]
            if step_version in step_upgrades:
                new_step = step_upgrades[step_version](step)

        new_steps.append(new_step)

    # Convert the new steps in the correct format
    new_steps_json = {
        str(i + 1): step for i, step in enumerate(new_steps)
    }

    return {
        'version': __version__,
        'steps': new_steps_json
    }