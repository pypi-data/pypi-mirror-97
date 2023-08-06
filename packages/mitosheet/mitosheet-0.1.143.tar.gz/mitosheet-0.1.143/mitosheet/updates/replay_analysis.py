#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Replays an existing analysis onto the sheet
"""

from copy import copy


from mitosheet.utils import get_new_step_id
from mitosheet.steps.filter import execute_filter_column
from mitosheet.save_utils import read_and_upgrade_analysis
from mitosheet.steps import STEP_TYPE_TO_STEP
from mitosheet.errors import make_execution_error


REPLAY_ANALYSIS_UPDATE_EVENT = 'replay_analysis_update'
REPLAY_ANALYSIS_UPDATE_PARAMS = [
    'analysis_name',
    'import_summaries',
    'clear_existing_analysis',
]

def execute_replay_analysis_update(
        wsc,
        analysis_name,
        import_summaries,
        clear_existing_analysis
    ):
    """
    This function reapplies all the steps summarized in the passed step summaries, 
    which come from a saved analysis. 

    If any of the step summaries fails, this function tries to roll back to before
    it applied any of the stems

    If clear_existing_analysis is set to true, then this will clear the entire widget
    state container (except the initalize step) before applying the saved analysis.
    """ 
    # We only keep the intialize step only
    if clear_existing_analysis:
        wsc.steps = wsc.steps[:1]

    # If we're getting an event telling us to update, we read in the steps from the file
    analysis = read_and_upgrade_analysis(analysis_name)

    # When replaying an analysis with import events, you can also send over
    # new params to the import events to replace them. We replace them in the steps here
    if import_summaries is not None:
        for step_idx, params in import_summaries.items():
            for key, value in params.items():
                analysis['steps'][step_idx][key] = value  

    # We make a shallow copy of the steps, as none of the objects
    # will be changed by the step summaries we apply   
    old_steps = copy(wsc.steps)
    
    try:
        for _, step_summary in analysis['steps'].items():

            curr_step = wsc.steps[-1]

            step_type = step_summary['step_type']

            step_obj = STEP_TYPE_TO_STEP[step_type]

            # Get the params for this event
            params = {key: value for key, value in step_summary.items() if key in step_obj['params']}

            # If it's filter, we need to do a lot of extra work
            # so we sent it into the execute function directly
            if step_obj['step_type'] == 'filter_column':
                execute_filter_column(
                    wsc,
                    **params
                )
                wsc.curr_step_idx = len(wsc.steps) - 1
                # We always make a new step, so we also save the id of this step
                wsc.curr_step['step_id'] = get_new_step_id()
                continue 


            # Actually execute this event
            new_step = step_obj['execute'](curr_step, **params)
            
            # Save the params for this event
            for key, value in params.items():
                new_step[key] = value

            # Every step also needs an id, which we add
            # TODO: in the future, we should functionalize (and unify) the running of
            # steps, so we don't have to remember to do this everywhere
            new_step['step_id'] = get_new_step_id()

            wsc.steps.append(new_step)
            wsc.curr_step_idx = len(wsc.steps) - 1

    except Exception as e:
        print(e)
        # We remove all applied steps if there was an error
        wsc.steps = old_steps
        wsc.curr_step_idx = len(old_steps) - 1

        # And report a generic error to the user
        raise make_execution_error()


REPLAY_ANALYSIS_UPDATE = {
    'event_type': REPLAY_ANALYSIS_UPDATE_EVENT,
    'params': REPLAY_ANALYSIS_UPDATE_PARAMS,
    'execute': execute_replay_analysis_update
}