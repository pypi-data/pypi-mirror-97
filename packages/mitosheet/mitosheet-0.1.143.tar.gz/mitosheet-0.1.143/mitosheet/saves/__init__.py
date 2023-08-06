#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains a list of all the saved analyses that we store in code, for usage 
in the great big Mito machine. 

Just kidding. It's so we can easily distribute them without a ton of extra 
work and having to worry about eventually changing the .mito file. 
"""

from mitosheet.saves.mito_simple_raw_import import MITO_SIMPLE_RAW_IMPORT_SAVE
from mitosheet.saves.tutorial_v3.mito_tutorial_checkpoint_2 import MITO_TUTORIAL_CHECKPOINT_2
from mitosheet.saves.tutorial_v3.mito_tutorial_checkpoint_3 import MITO_TUTORIAL_CHECKPOINT_3
from mitosheet.saves.tutorial_v3.mito_tutorial_checkpoint_4 import MITO_TUTORIAL_CHECKPOINT_4
from mitosheet.saves.tutorial_v3.mito_tutorial_checkpoint_5 import MITO_TUTORIAL_CHECKPOINT_5
from mitosheet.saves.tutorial_v3.mito_tutorial_checkpoint_6 import MITO_TUTORIAL_CHECKPOINT_6

SAVES = {
    MITO_SIMPLE_RAW_IMPORT_SAVE['name']: MITO_SIMPLE_RAW_IMPORT_SAVE['saved_analysis'],
    MITO_TUTORIAL_CHECKPOINT_2['name']: MITO_TUTORIAL_CHECKPOINT_2['saved_analysis'],
    MITO_TUTORIAL_CHECKPOINT_3['name']: MITO_TUTORIAL_CHECKPOINT_3['saved_analysis'],
    MITO_TUTORIAL_CHECKPOINT_4['name']: MITO_TUTORIAL_CHECKPOINT_4['saved_analysis'],
    MITO_TUTORIAL_CHECKPOINT_5['name']: MITO_TUTORIAL_CHECKPOINT_5['saved_analysis'],
    MITO_TUTORIAL_CHECKPOINT_6['name']: MITO_TUTORIAL_CHECKPOINT_6['saved_analysis']
}