#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains interfaces and helpers for dealing with the user profile.

Currently, the users profile is stored on disk where Mito is installed, 
but in the future we will support other profile storing locations (e.g.
on a server, so that users can log into a webapp!)
"""
import getpass
import os
import uuid
import json
from datetime import datetime

from mitosheet.mito_analytics import identify

from mitosheet._version import __version__
from mitosheet.user.user_utils import (
    get_user_field, set_user_field,
    MITO_FOLDER, USER_JSON_PATH
)
from mitosheet.mito_analytics import analytics



# This is the default user json object
USER_JSON_DEFAULT = {
    'user_json_version': 1,
    'static_user_id': '',
    'user_email': '',
    'mitosheet_current_version': __version__,
    'mitosheet_last_upgraded_date': datetime.today().strftime('%Y-%m-%d'),
    'mitosheet_last_five_usages': [datetime.today().strftime('%Y-%m-%d')]
}

def get_random_id():
    """
    Creates a new random ID for the user, which for any given user,
    should only happen once.
    """
    return str(uuid.uuid1())


def is_on_kuberentes_mito():
    """
    Returns True if the user is on Kuberentes Mito
    """
    user = getpass.getuser()
    return user == 'jovyan'


def is_local_deployment():
    """
    Helper function for figuring out if this a local deployment or a
    Mito server deployment
    """
    return not is_on_kuberentes_mito()  


def initialize_user():
    """
    Internal helper function that gets called every time mitosheet 
    is imported.

    It:
    1. Creates a ~/.mito folder, if it does not exist.
    2. Creates new, default user.json file if it does not exist, taking
       special care to do things properly if we're in a CI enviornment.
    3. Updates the user.json file with any new variables, as well as logging
       this usage, and any potential upgrades that may have occured
    """
    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    # We only create a user.json file if it does not exist
    if not os.path.exists(USER_JSON_PATH):
        # First, we write an empty default object
        with open(USER_JSON_PATH, 'w+') as f:
            f.write(json.dumps(USER_JSON_DEFAULT))

        # Then, we create a new static id and capture the email for the user. 
        # We take special care to put all the CI enviornments 
        # (e.g. Github actions) under one ID and email
        if 'CI' in os.environ and os.environ['CI'] is not None:
            static_user_id = 'github_action'
            user_email = 'github@action.com'
        else:
            static_user_id = get_random_id()
            # Then, we check if the user is on the server. If they are are on the server, then we
            # can get their email as their JUPYTERHUB_USER. If they are not on the server, then we set
            # their email as empty for now
            if is_on_kuberentes_mito():
                user_email = os.getenv('JUPYTERHUB_USER')
            else:
                user_email = ''

        set_user_field('static_user_id', static_user_id)
        set_user_field('user_email', user_email)


    # Then we just make sure that the user.json has all the fields it needs defined
    # and if they are not defined, it sets them to the default values
    for field, default_value in USER_JSON_DEFAULT.items():
        if get_user_field(field) is None:
            set_user_field(field, default_value)

    # Then, we check if Mito has been upgraded since it was last imported
    # and if it has been upgraded, we upgrade the version and the upgrade date
    if get_user_field('mitosheet_current_version') != __version__:
        set_user_field('mitosheet_current_version', __version__)
        set_user_field('mitosheet_last_upgraded_date', datetime.today().strftime('%Y-%m-%d'))

    # We also note this import as a Mito usage, making sure to only 
    # mark this as usage once per day
    last_five_usages = get_user_field('mitosheet_last_five_usages')
    if len(last_five_usages) == 0 or last_five_usages[-1] != datetime.today().strftime('%Y-%m-%d'):
        last_five_usages.append(datetime.today().strftime('%Y-%m-%d'))
    # Then, we take the 5 most recent (or as many as there are), and save them
    if len(last_five_usages) < 5:
        most_recent_five = last_five_usages
    else: 
        most_recent_five = last_five_usages[-5:]
    set_user_field('mitosheet_last_five_usages', most_recent_five)

    # Then, we identify the user, always
    identify()

def should_upgrade_mitosheet():
    """
    A helper function that calculates if a user should upgrade,
    which in practice does this with the following heuristic:
    1. If the user has not upgraded in two weeks, then we always reccomend that the user
       upgrades.
    2. If the user has used the tool 4 times since they last upgraded, then we also reccomend
       that they upgrade

    NOTE: this should always return false if it is not a local installation, for obvious
    reasons.

    The motivation here is just: we want them to upgrade frequently, but we also don't
    want to just bombard them with upgrade messages. This is a nice middle ground.
    """
    if not is_local_deployment():
        return False

    mitosheet_last_upgraded_date = datetime.strptime(get_user_field('mitosheet_last_upgraded_date'), '%Y-%m-%d')
    mitosheet_last_five_usages = [datetime.strptime(usage, '%Y-%m-%d') for usage in get_user_field('mitosheet_last_five_usages')]

    current_time = datetime.now()
    # Condition (1)
    if (current_time - mitosheet_last_upgraded_date).days > 14:
        return True
    # Condition (2)
    elif len(mitosheet_last_five_usages) >= 4:
        # As this list is chronological, we just need to check 4 back
        if mitosheet_last_five_usages[-4] > mitosheet_last_upgraded_date:
            return True

    return False