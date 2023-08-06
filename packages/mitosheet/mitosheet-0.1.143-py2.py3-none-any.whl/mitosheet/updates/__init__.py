#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains the exports for update events, which are events that manipulate
the steps in some way, but do not _just generate a step_ (see ../steps for
more information about steps).

Examples of this sort of event are:
- Lots of steps being replayed from the front-end.
- A user undoing an existing step. 
"""

from mitosheet.updates.undo import UNDO_UPDATE
from mitosheet.updates.df_names import DF_NAMES_UPDATE
from mitosheet.updates.save_analysis import SAVE_ANALYSIS_UPDATE
from mitosheet.updates.replay_analysis import REPLAY_ANALYSIS_UPDATE
from mitosheet.updates.delete_saved_analysis import DELETE_SAVED_ANALYSIS_UPDATE
from mitosheet.updates.rename_saved_analysis import RENAME_SAVED_ANALYSIS_UPDATE
from mitosheet.updates.signup import SIGNUP_UPDATE
from mitosheet.updates.checkout_step_by_idx import CHECKOUT_STEP_BY_IDX_UPDATE

# All update events must be listed in this variable.
UPDATES = [
    UNDO_UPDATE,
    DF_NAMES_UPDATE,
    SAVE_ANALYSIS_UPDATE,
    REPLAY_ANALYSIS_UPDATE,
    RENAME_SAVED_ANALYSIS_UPDATE,
    DELETE_SAVED_ANALYSIS_UPDATE,
    SIGNUP_UPDATE,
    CHECKOUT_STEP_BY_IDX_UPDATE
]