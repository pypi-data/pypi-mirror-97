#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for edit events.
"""
import os
from mitosheet.transpiler.transpile import transpile
import pytest
import pandas as pd
import json
import random

from mitosheet.example import sheet
from mitosheet.tests.test_utils import create_mito_wrapper, create_mito_wrapper_dfs

from mitosheet.save_utils import SAVED_ANALYSIS_FOLDER, write_analysis, read_analysis, read_saved_analysis_names, write_saved_analysis
from mitosheet.errors import EditError
from _pytest._code import ExceptionInfo

# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_recover_analysis(b_value, b_formula):
    mito = create_mito_wrapper([1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df = pd.DataFrame(data={'A': [1]})
    new_mito = create_mito_wrapper_dfs(df)
    new_mito.replay_analysis(analysis_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.mito_widget.widget_state_container.dfs[0]['B'].tolist() == [b_value]
    assert new_mito.mito_widget.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])


# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_persist_analysis_multi_sheet(b_value, b_formula):
    mito = create_mito_wrapper([1], sheet_two_A_data=[1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    mito.set_formula(b_formula, 1, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})
    df2 = pd.DataFrame(data={'A': [1]})

    new_mito = create_mito_wrapper_dfs(df1, df2)
    new_mito.replay_analysis(analysis_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.mito_widget.widget_state_container.dfs[0]['B'].tolist() == [b_value]

    assert curr_step['column_metatype'][1]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][1]['B'] == b_formula
    assert new_mito.mito_widget.widget_state_container.dfs[1]['B'].tolist() == [b_value]
    
    assert new_mito.mito_widget.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])
    assert new_mito.mito_widget.code_json == mito.mito_widget.code_json


def test_persist_rename_column():
    mito = create_mito_wrapper([1])
    mito.rename_column(0, 'A', 'NEW_COLUMN')

    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(analysis_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step

    assert curr_step['dfs'][0].equals(pd.DataFrame(data={'NEW_COLUMN': [1]}))

def test_persisit_delete_column():
    mito = create_mito_wrapper([1])
    mito.delete_column(0, 'A')

    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(analysis_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step

    assert len(curr_step['dfs'][0].keys()) == 0


def test_save_analysis_update():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')
    mito.delete_column(0, 'A')

    random_name = 'UUID-test_save' + str(random.random())

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(random_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step
    assert curr_step['dfs'][0].keys() == ['B']

def test_save_analysis_update_and_overwrite():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')

    random_name = 'UUID-test_save' + str(random.random())

    # Save it once
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    mito.delete_column(0, 'A')
    mito.delete_column(0, 'B')

    # Save it again
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(random_name)

    curr_step = new_mito.mito_widget.widget_state_container.curr_step
    assert len(curr_step['dfs'][0].keys()) == 0

def test_saved_analysis_in_saved_analysis():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')

    random_name = 'test_save' + str(random.random())

    # Save it once
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    saved_analysis_names = read_saved_analysis_names()
    assert random_name in saved_analysis_names

def test_failed_replay_does_not_add_steps():
    # Make an analysis and save it
    mito = create_mito_wrapper([1])
    mito.set_formula('=A + 1', 0, 'B', add_column=True)
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    df = pd.DataFrame(data={'A': [1], 'B': [3]})
    new_mito = create_mito_wrapper_dfs(df)

    new_mito.replay_analysis(random_name)

    # Make sure no step was added
    assert len(new_mito.mito_widget.widget_state_container.steps) == 1



def test_pivot_by_replays():
    # Make an analysis and save it
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.pivot_sheet(
        0, 
        ['Name'],
        [],
        {'Height': 'sum'}
    )
    
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    new_mito = create_mito_wrapper_dfs(df1)

    new_mito.replay_analysis(random_name)

    # Make sure no step was added
    wsc = new_mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.steps[1]['step_type'] == 'pivot'
    assert len(wsc.curr_step['dfs']) == 2
    assert wsc.curr_step['dfs'][1].equals(
        pd.DataFrame(data={'Name': ['Nate'], 'Height': [9]})
    )


def test_merge_replays():
    # Make an analysis and save it
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Jake'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.merge_sheets(
        0, 
        'Name',
        ['Name', 'Height'],
        0,
        'Name',
        ['Name', 'Height']
    )
    
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(random_name)

    # Make sure no step was added
    wsc = new_mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.steps[1]['step_type'] == 'merge'
    assert len(wsc.curr_step['dfs']) == 2
    assert wsc.curr_step['dfs'][1].equals(
        pd.DataFrame(data={'Name': ['Nate', 'Jake'], 'Height_df1': [4, 5], 'Height_df1_2': [4, 5]})
    )

TEST_FILE_PATH = 'test_file.csv'

def test_import_replays():
    df = pd.DataFrame(data={'A': [1, 2, 3], 'B': [2, 3, 4]})
    df.to_csv(TEST_FILE_PATH, index=False)

    # Create with no dataframes
    mito = create_mito_wrapper_dfs()
    # And then import just a test file
    mito.simple_import([TEST_FILE_PATH])
    
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    new_mito = create_mito_wrapper_dfs()
    new_mito.replay_analysis(random_name)

    os.remove(TEST_FILE_PATH)

    # Make sure no step was added
    wsc = new_mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.steps[1]['step_type'] == 'simple_import'
    assert len(wsc.curr_step['dfs']) == 1
    assert wsc.curr_step['dfs'][0].equals(
        df
    )


def test_replay_analysis_does_not_make_removed_columns():
    df1 = pd.DataFrame(data={'A': [123], 'B': [1234]})
    mito = create_mito_wrapper_dfs(df1)

    mito.add_column(0, 'C')

    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe with no column B, and it shouldn't recreate B
    df1 = pd.DataFrame(data={'A': [123]})
    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(random_name)


    assert list(new_mito.mito_widget.widget_state_container.dfs[0].keys()) == ['A', 'C']


def test_upgrades_old_analysis_before_replaying_it():
    write_saved_analysis(
        f'{SAVED_ANALYSIS_FOLDER}/UUID-test-upgrade.json',
        {"1": {"step_version": 1, "step_type": "group", "sheet_index": 0, "group_rows": ["A"], "group_columns": [], "values": {"B": "sum"}}},
        version='0.1.60'
    )

    df = pd.DataFrame({'A': [123], 'B': [123]})
    new_mito = create_mito_wrapper_dfs(df)
    new_mito.replay_analysis('UUID-test-upgrade')

    # This pivot happens to be an identity!
    assert new_mito.mito_widget.widget_state_container.dfs[1].equals(
        df
    )

def test_replay_analysis_can_overwrite_entire_analysis():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    df1 = pd.DataFrame(data={'A': [123]})
    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.rename_column(0, 'A', 'C')
    new_mito.replay_analysis(random_name, clear_existing_analysis=True)
    
    curr_step = new_mito.mito_widget.widget_state_container.curr_step
    assert len(new_mito.mito_widget.widget_state_container.steps) == 2
    assert curr_step['dfs'][0].equals(
        pd.DataFrame({'B': [123]})
    )

def test_rename_analysis():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name = 'UUID-test_save' + str(random.random())
    new_randome_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'rename_analysis_update',
        'old_analysis_name': random_name,
        'new_analysis_name': new_randome_name
    })

    df1 = pd.DataFrame(data={'A': [123]})
    new_mito = create_mito_wrapper_dfs(df1)
    new_mito.replay_analysis(new_randome_name, clear_existing_analysis=True)
    
    curr_step = new_mito.mito_widget.widget_state_container.curr_step
    assert len(new_mito.mito_widget.widget_state_container.steps) == 2
    assert curr_step['dfs'][0].equals(
        pd.DataFrame({'B': [123]})
    )


def test_rename_analysis_with_non_existant_analysis():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name
    })

    new_random_name_one = 'UUID-test_save' + str(random.random())
    new_random_name_two = 'UUID-test_save' + str(random.random())

    with pytest.raises(Exception) as e:
        # We call the event handler directly, so we can catch the error
        mito.mito_widget.widget_state_container.handle_update_event({
            'event': 'update_event',
            'type': 'rename_analysis_update',
            'old_analysis_name': new_random_name_one,
            'new_analysis_name': new_random_name_two
        })
    assert(str(e.value)) == f'Invalid rename, with old and new analysis are {new_random_name_one} and {new_random_name_two}'


def test_rename_analysis_with_already_existing_analysis():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name_one = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name_one
    })

    random_name_two = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name_two
    })

    with pytest.raises(Exception) as e:
        # We call the event handler directly, so we can catch the error
        mito.mito_widget.widget_state_container.handle_update_event({
            'event': 'update_event',
            'type': 'rename_analysis_update',
            'old_analysis_name': random_name_one,
            'new_analysis_name': random_name_two
        })
    
    assert(str(e.value)) == f'Invalid rename, with old and new analysis are {random_name_one} and {random_name_two}'


def test_delete_analysis_deletes():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name_one = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name_one
    })

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'delete_analysis_update',
        'analysis_name': random_name_one
    })

    assert read_analysis(random_name_one) is None


def test_delete_analysis_fails_on_nonexistant_analysis():
    df = pd.DataFrame({'A': [123]})
    mito = create_mito_wrapper_dfs(df)
    mito.rename_column(0, 'A', 'B')

    random_name_one = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis_update',
        'analysis_name': random_name_one
    })

    with pytest.raises(Exception) as e:
        # We call the event handler directly, so we can catch the error
        mito.mito_widget.widget_state_container.handle_update_event({
            'event': 'update_event',
            'type': 'delete_analysis_update',
            'analysis_name': random_name_one + "1",
        })
        
    assert str(e.value) == f'Cannot delete {random_name_one + "1"} as it does not exist'
