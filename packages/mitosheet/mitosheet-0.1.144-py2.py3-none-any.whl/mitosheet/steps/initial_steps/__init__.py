#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Initial steps are steps that:
1. Are run at the start of every Mito analysis, (e.g. right after
   a user calls mitosheet.sheet).
2. Require no user input to run - and are just always run - and so
   we don't necessarily need to save them when we write out an 
   analysis.

Currently, there are two initial steps:
1. Renaming column headers to be a valid Mito format. 
2. Creating the initial "step."
"""

from mitosheet.steps.initial_steps.initalize import INITIALIZE_STEP
from mitosheet.steps.initial_steps.initial_rename import INITIAL_RENAME_STEP

INITIAL_STEPS = [
    INITIALIZE_STEP,
    INITIAL_RENAME_STEP
]