#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A signup update, sets the user's email as the user_email in user.json
"""

from mitosheet.mito_analytics import identify
from mitosheet.user.user_utils import set_user_field


SIGNUP_EVENT = 'signup_update'
SIGNUP_PARAMS = ['user_email']


def execute_signup_update(wsc, user_email):
    """
    The function responsible for signing in the user.
    """
    # Set the user_email in user.json
    set_user_field('user_email', user_email)

    # Identify the user with their new email
    identify()

SIGNUP_UPDATE = {
    'event_type': SIGNUP_EVENT,
    'params': SIGNUP_PARAMS,
    'execute': execute_signup_update
}