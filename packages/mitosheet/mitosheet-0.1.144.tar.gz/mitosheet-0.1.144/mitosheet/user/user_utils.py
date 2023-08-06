#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions for getting and setting the user profile 
in user.json
"""

from copy import deepcopy
import os
import json

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The path of the user.json file
USER_JSON_PATH = os.path.join(MITO_FOLDER, 'user.json')


def get_user_field(field):
    """
    Returns the value stored at field in the user.json file.
    """
    try:
        with open(USER_JSON_PATH) as f:
            return json.load(f)[field]
    except: 
        return None

def set_user_field(field, value):
    """
    Updates the value of a specific feild in user.json
    """
    with open(USER_JSON_PATH, 'r') as user_file_old:
        old_user_json = json.load(user_file_old)
        old_user_json[field] = value
        with open(USER_JSON_PATH, 'w+') as f:
            f.write(json.dumps(old_user_json))