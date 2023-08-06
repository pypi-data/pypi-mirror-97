#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the transpile function, which takes the backend widget
container and generates transpiled Python code.
"""
from itertools import zip_longest

from mitosheet.steps import STEPS
from mitosheet.steps.initial_steps.initial_rename import transpile_initial_rename_step

from mitosheet.steps.column_steps.add_column import ADD_COLUMN_STEP_TYPE
from mitosheet.steps.column_steps.set_column_formula import SET_COLUMN_FORMULA_STEP_TYPE


IN_PREVIOUS_STEP_COMMENT = '# You\'re viewing a previous step. Click fast forward in the Mitosheet above to see the full analysis.'

def get_steps_to_ignore(steps):
    """
    We ignore a step if:
    1. It is a create a column step,
    2. That is followed by a step that sets that column formula
    """
    steps_to_ignore = []

    step_pairs = zip_longest(steps, steps[1:])

    for step_idx, (first_step, second_step) in enumerate(step_pairs):
        if first_step is None or second_step is None:
            continue

        if first_step['step_type'] == ADD_COLUMN_STEP_TYPE and second_step['step_type'] == SET_COLUMN_FORMULA_STEP_TYPE:
            if first_step['column_header'] == second_step['column_header']:
                steps_to_ignore.append(step_idx)

    return steps_to_ignore


def transpile(widget_state_container):
    """
    Takes the Python code in the widget_state_container and linearizes it
    so it can be consumed by the front-end. 
    
    When there are multiple sheets, the first sheets code is first, followed
    by the second sheets code, etc. 
    """

    code = []
    filled_steps = 1

    # First, we manually code an initial rename_step, which occurs
    initial_rename_step = transpile_initial_rename_step(widget_state_container)
    if len(initial_rename_step) > 0:
        code.append("# Step 1 (rename headers to make them work with Mito)")
        code.extend(initial_rename_step)
        filled_steps += 1

    steps_to_ignore = get_steps_to_ignore(widget_state_container.steps)

    # We only transpile up to the currently checked out step
    for step_idx, step in enumerate(widget_state_container.steps[:widget_state_container.curr_step_idx + 1]):
        if step_idx in steps_to_ignore:
            continue

        step_code = [f'# Step {filled_steps}']

        for new_step in STEPS:
            if step['step_type'] == new_step['step_type']:
                # Get the params for this event
                params = {key: value for key, value in step.items() if key in new_step['params']}
                # Actually execute this event
                step_code.extend(new_step['transpile'](
                    step,
                    **params
                ))

        # If we don't write any code, skip
        if len(step_code) == 1:
            continue

        filled_steps += 1
        code.extend(step_code)

    # If we have a historical step checked out, then we add a comment letting
    # the user know this is the case
    if widget_state_container.curr_step_idx != len(widget_state_container.steps) - 1:
        code.append(IN_PREVIOUS_STEP_COMMENT)

    return {
        'imports': f'from mitosheet import *',
        'code': code
    }