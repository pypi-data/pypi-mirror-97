#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A undo update, which removes the most recent step from
the sheet. 
"""

UNDO_EVENT = 'undo'
UNDO_PARAMS = []

def execute_undo_update(wsc):
    """
    The function responsible for updating the widget state container
    by removing the most recent step.

    If there is no most recent step, does nothing.
    """

    if len(wsc.steps) == 1:
        return 

    # Pop off the last element
    wsc.steps.pop()

    # TODO: there is currently a bug with this event when we are rolled back, this will
    # jump us to the end of the steps
    wsc.curr_step_idx = len(wsc.steps) - 1


"""
This object wraps all the information
that is needed for a undo step!
"""
UNDO_UPDATE = {
    'event_type': UNDO_EVENT,
    'params': UNDO_PARAMS,
    'execute': execute_undo_update
}





