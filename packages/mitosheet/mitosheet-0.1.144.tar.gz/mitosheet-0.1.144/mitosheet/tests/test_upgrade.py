#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
from mitosheet._version import __version__
from mitosheet.upgrade import (
    is_prev_version
)

from mitosheet.save_utils import (
    SAVED_ANALYSIS_FOLDER, write_saved_analysis,
    read_and_upgrade_analysis
)


PREV_TESTS = [
    ('0.1.61', '0.1.62', True),
    ('0.1.61', '0.1.610', True),
    ('0.1.62', '0.1.62', False),
    ('0.2.61', '0.1.62', False),
    ('0.2.62', '0.2.62', False),
]
@pytest.mark.parametrize("prev, curr, result", PREV_TESTS)
def test_prev_analysis_returns_correct_results(prev, curr, result):
    assert is_prev_version(prev, curr_version=curr) == result

TEST_ANALYSIS_NAME = 'UUID-test_analysis'
TEST_FILE = f'{SAVED_ANALYSIS_FOLDER}/{TEST_ANALYSIS_NAME}.json'

UPGRADE_TESTS = [
    # Simple column add step. Nothing should be changed
    (
        {
            "version": "0.1.59", "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "["}}
        },
        {
            "version": "0.1.59", "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "["}}
        }
    ),
    # Add columns, set formulas, and delete
    (
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "D"}, "2": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "E"}, "3": {"step_version": 1, "step_type": "set_column_formula", "sheet_index": 0, "column_header": "D", "old_formula": "=0", "new_formula": "=OFFSET(B, -1)"}, "4": {"step_version": 1, "step_type": "delete_column", "sheet_index": 0, "column_header": "D"}}
        },
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "D"}, "2": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "E"}, "3": {"step_version": 1, "step_type": "set_column_formula", "sheet_index": 0, "column_header": "D", "old_formula": "=0", "new_formula": "=OFFSET(B, -1)"}, "4": {"step_version": 1, "step_type": "delete_column", "sheet_index": 0, "column_header": "D"}}
        }
    ),
    # A merge should not be upgraded
    (
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "merge", "sheet_index_one": 0, "sheet_index_two": 1, "merge_key_one": "Name", "merge_key_two": "Name", "selected_columns_one": ["Name", "Number"], "selected_columns_two": ["Name", "Sign"]}, "2": {"step_version": 1, "step_type": "sort", "sheet_index": 2, "column_header": "Number", "sort_direction": "descending"}}
        },
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "merge", "sheet_index_one": 0, "sheet_index_two": 1, "merge_key_one": "Name", "merge_key_two": "Name", "selected_columns_one": ["Name", "Number"], "selected_columns_two": ["Name", "Sign"]}, "2": {"step_version": 1, "step_type": "sort", "sheet_index": 2, "column_header": "Number", "sort_direction": "descending"}}
        },
    ),
    # Test filter and sort
    (
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "filter_column", "sheet_index": 0, "column_header": "String", "filters": [{"type": "string", "condition": "contains", "value": "1"}], "operator": "And"}, "2": {"step_version": 1, "step_type": "sort", "sheet_index": 0, "column_header": "String", "sort_direction": "ascending"}}
        },
        {
            "version": "0.1.55", 
            "steps": {"1": {"step_version": 1, "step_type": "filter_column", "sheet_index": 0, "column_header": "String", "filters": [{"type": "string", "condition": "contains", "value": "1"}], "operator": "And"}, "2": {"step_version": 1, "step_type": "sort", "sheet_index": 0, "column_header": "String", "sort_direction": "ascending"}}
        },
    ),
    # Single group step, it should should be upgraded to a pivot
    (
        {
            "version": "0.1.54", 
            "steps": {"1": {"step_version": 1, "step_type": "group", "sheet_index": 0, "group_rows": ["Name"], "group_columns": [], "values": {"Height": "sum"}}}
        },
        {
            "version": __version__, 
            "steps": {"1": {"step_version": 2, "step_type": "pivot", "sheet_index": 0, "pivot_rows": ["Name"], "pivot_columns": [], "values": {"Height": "sum"}}}
        }
    ), 
    # Ends in a group step, should be upgraded to a pivot
    (
        {
            "version": "0.1.54", 
            "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "B"}, "2": {"step_version": 1, "step_type": "set_column_formula", "sheet_index": 0, "column_header": "B", "old_formula": "=0", "new_formula": "=1"}, "3": {"step_version": 1, "step_type": "group", "sheet_index": 0, "group_rows": ["Name"], "group_columns": ["DORK"], "values": {"Height": "sum"}}}
        },
        {
            "version": __version__, 
            "steps": {"1": {"step_version": 1, "step_type": "add_column", "sheet_index": 0, "column_header": "B"}, "2": {"step_version": 1, "step_type": "set_column_formula", "sheet_index": 0, "column_header": "B", "old_formula": "=0", "new_formula": "=1"}, "3": {"step_version": 2, "step_type": "pivot", "sheet_index": 0, "pivot_rows": ["Name"], "pivot_columns": ["DORK"], "values": {"Height": "sum"}}}
        },
    ), 
    # A group step in the middle, should be upgraded to a pivot
    (
        {
            "version": "0.1.60", 
            "steps": {"1": {"step_version": 1, "step_type": "simple_import", "file_names": ["NamesNew.csv"]}, "2": {"step_version": 1, "step_type": "group", "sheet_index": 0, "group_rows": [], "group_columns": ["Ha", 'Ha'], "values": {}}, "3": {"step_version": 1, "step_type": "simple_import", "file_names": ["NamesNew.csv"]}}
        },
        {
            "version": __version__, 
            "steps": {"1": {"step_version": 1, "step_type": "simple_import", "file_names": ["NamesNew.csv"]}, "2": {"step_version": 2, "step_type": "pivot", "sheet_index": 0, "pivot_rows": [], "pivot_columns": ["Ha", "Ha"], "values": {}}, "3": {"step_version": 1, "step_type": "simple_import", "file_names": ["NamesNew.csv"]}}
        },
    )
]
@pytest.mark.parametrize("old, new", UPGRADE_TESTS)
def test_does_not_upgrade_current_analysis(old, new):
    write_saved_analysis(TEST_FILE, old['steps'], version=old['version'])
    assert read_and_upgrade_analysis(TEST_ANALYSIS_NAME) == new


# TODO: 
# 2. Add a test for _each_ of the step types!