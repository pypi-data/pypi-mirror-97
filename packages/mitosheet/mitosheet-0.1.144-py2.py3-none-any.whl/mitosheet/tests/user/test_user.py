#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for the user.json file, making sure it upgrades properly,
and that it can handle the various undefined versions of user.json that exist.
"""
from datetime import datetime, timedelta
import pytest
import json
import os

from mitosheet._version import __version__
from mitosheet.user.user import initialize_user, should_upgrade_mitosheet
from mitosheet.user.user_utils import USER_JSON_PATH, get_user_field

@pytest.fixture(scope="module", autouse=True)
def cleanup_files():
    """
    This fixture reads in the original user.json file that exists before these tests are
    run, deletes it, and then recreates it at the end. This allows us to test what happens 
    when the user.json file is in various states of out of date and disrepair.
    """
    with open(USER_JSON_PATH, 'r') as f:
        user_json = json.loads(f.read())

    os.remove(USER_JSON_PATH)

    yield # All tests in this user module run right here

    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps(user_json))


def test_initialize_user_creates_json_when_empty():
    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert len(get_user_field('static_user_id')) > 0
    assert len(get_user_field('user_email')) == 0 or (get_user_field('user_email') == 'github@action.com' and 'CI' in os.environ)
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == [datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)


def test_initialize_upgrades_user_when_old_version():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'static_user_id': 'github_action',
            'user_email': 'github@action.com'
        }))

    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert get_user_field('static_user_id') == 'github_action'
    assert get_user_field('user_email') == 'github@action.com'
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == [datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)


def test_initalize_detects_new_usage_when_less_than_five():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': datetime.today().strftime('%Y-%m-%d'),
            'mitosheet_last_five_usages': ['2020-12-1']
        }))

    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert get_user_field('static_user_id') == 'github_action'
    assert get_user_field('user_email') == 'github@action.com'
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == ['2020-12-1', datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)


def test_initalize_detects_new_usage_when_five():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': datetime.today().strftime('%Y-%m-%d'),
            'mitosheet_last_five_usages': ['2020-12-1', '2020-12-2', '2020-12-3', '2020-12-4', '2020-12-5']
        }))

    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert get_user_field('static_user_id') == 'github_action'
    assert get_user_field('user_email') == 'github@action.com'
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == ['2020-12-2', '2020-12-3', '2020-12-4', '2020-12-5', datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)


def test_initialize_user_only_stores_day_once():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': datetime.today().strftime('%Y-%m-%d'),
            'mitosheet_last_five_usages': ['2020-12-1', '2020-12-2', '2020-12-3', '2020-12-4', datetime.today().strftime('%Y-%m-%d')]
        }))

    initialize_user()
    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert get_user_field('static_user_id') == 'github_action'
    assert get_user_field('user_email') == 'github@action.com'
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == ['2020-12-1', '2020-12-2', '2020-12-3', '2020-12-4', datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)

    
def test_initalize_detects_when_mito_upgraded():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': '0.1.100',
            'mitosheet_last_upgraded_date': '2020-12-1',
            'mitosheet_last_five_usages': ['2020-12-1', '2020-12-2', '2020-12-3', '2020-12-4', '2020-12-5']
        }))

    initialize_user()

    assert os.path.exists(USER_JSON_PATH)
    assert get_user_field('user_json_version') == 1
    assert get_user_field('static_user_id') == 'github_action'
    assert get_user_field('user_email') == 'github@action.com'
    assert get_user_field('mitosheet_current_version') == __version__
    assert get_user_field('mitosheet_last_upgraded_date') == datetime.today().strftime('%Y-%m-%d')
    assert get_user_field('mitosheet_last_five_usages') == ['2020-12-2', '2020-12-3', '2020-12-4', '2020-12-5', datetime.today().strftime('%Y-%m-%d')]

    os.remove(USER_JSON_PATH)


def test_should_not_upgrade_on_first_creation():
    initialize_user()
    assert not should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_not_upgrade_with_less_than_four_usages():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': '0.1.100',
            'mitosheet_last_upgraded_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'), # only 5 days ago,
            'mitosheet_last_five_usages': ['2020-12-1', '2020-12-2']
        }))

    initialize_user()
    assert not should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_upgrade_mitosheet_greater_than_two_weeks():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': '2020-12-2',
            'mitosheet_last_five_usages': ['2020-12-1', '2020-12-2']
        }))

    initialize_user()
    assert should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_upgrade_mitosheet_greater_than_two_weeks_and_five_usages_since_then():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': '2020-12-2',
            'mitosheet_last_five_usages': ['2020-12-3', '2020-12-4', '2020-12-5', '2020-12-6', '2020-12-7']
        }))

    initialize_user()
    assert should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_upgrade_mitosheet_greater_than_two_weeks_no_usage():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': '2020-12-2',
            'mitosheet_last_five_usages': []
        }))

    initialize_user()
    assert should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_upgrade_mitosheet_at_least_4_usages_since_last_upgrade():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'), # only 5 days ago
            'mitosheet_last_five_usages': [
                (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d'),
                (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'),
                (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
            ]
        }))

    initialize_user()
    assert should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


def test_should_not_upgrade_mitosheet_more_than_4_usages_but_some_before_last_upgrade():
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps({
            'user_json_version': 1,
            'static_user_id': 'github_action',
            'user_email': 'github@action.com',
            'mitosheet_current_version': __version__,
            'mitosheet_last_upgraded_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'), # only 5 days ago
            'mitosheet_last_five_usages': [
                (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d'),
                (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'),
                (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
            ]
        }))

    initialize_user()
    assert not should_upgrade_mitosheet()
    os.remove(USER_JSON_PATH)


