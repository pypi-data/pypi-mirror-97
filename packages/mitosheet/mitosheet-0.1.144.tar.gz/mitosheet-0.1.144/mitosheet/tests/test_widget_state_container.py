#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pandas as pd
import pytest

from mitosheet.utils import get_new_step_id
from mitosheet.errors import EditError
from mitosheet.widget_state_container import WidgetStateContainer
from mitosheet.steps.column_steps.add_column import execute_add_column_step
from mitosheet.tests.test_utils import create_mito_wrapper, create_mito_wrapper_dfs


def test_create_widget_state_container():
    df = pd.DataFrame(data={'A': [123]})
    wsc = WidgetStateContainer([df])
    assert wsc.curr_step_idx == 0
    
    assert wsc.curr_step['step_type'] == 'initialize'
    assert wsc.curr_step['column_metatype'] == [{'A': 'value'}]
    assert wsc.curr_step['column_spreadsheet_code'] == [{'A': ''}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}]
    assert wsc.curr_step['column_evaluation_graph'] == [{'A': set()}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}]
    assert wsc.curr_step['dfs'][0].equals(df)

def test_create_widget_state_container_multiple_dfs():
    df1 = pd.DataFrame(data={'A': [123]})
    df2 = pd.DataFrame(data={'A': [123]})

    wsc = WidgetStateContainer([df1, df2])
    assert wsc.curr_step_idx == 0
    assert wsc.curr_step['step_type'] == 'initialize'
    assert wsc.curr_step['column_metatype'] == [{'A': 'value'}, {'A': 'value'}]
    assert wsc.curr_step['column_spreadsheet_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['column_evaluation_graph'] == [{'A': set()}, {'A': set()}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['dfs'][0].equals(df1)
    assert wsc.curr_step['dfs'][1].equals(df2)

# We assume only column A exists
CELL_EDIT_ERRORS = [
    ('=HI()', 'unsupported_function_error'),
    ('=UPPER(HI())', 'unsupported_function_error'),
    ('=UPPER(HI())', 'unsupported_function_error'),
    ('=C', 'no_column_error'),
    ('=C + D', 'no_column_error'),
    ('=ABCDEFG', 'no_column_error'),
    ('=UPPER(C)', 'no_column_error'),
    ('=B', 'circular_reference_error'),
    ('=UPPER(A, 100)', 'execution_error'),
    ('=UPPER(LOWER(A, 100))', 'execution_error')
]

@pytest.mark.parametrize("formula,error_type", CELL_EDIT_ERRORS)
def test_widget_state_container_cell_edit_errors(formula,error_type):
    mito = create_mito_wrapper([123])
    mito.add_column(0, 'B')
    with pytest.raises(EditError) as e_info:
        mito.mito_widget.widget_state_container.handle_edit_event({
            'event': 'edit_event',
            'type': 'set_column_formula_edit',
            'step_id': get_new_step_id(),
            'sheet_index': 0,
            'column_header': 'B',
            'old_formula': '=0',
            'new_formula': formula
        })
    assert e_info.value.type_ == error_type

def test_column_exists_error():
    mito = create_mito_wrapper([123])
    mito.add_column(0, 'B')
    with pytest.raises(EditError) as e_info:
        execute_add_column_step(mito.mito_widget.widget_state_container.curr_step, 0, 'B')
    assert e_info.value.type_ == 'column_exists_error'

def test_wrong_column_metatype():
    mito = create_mito_wrapper([123])
    mito.add_column(0, 'B')
    with pytest.raises(EditError) as e_info:
        mito.mito_widget.widget_state_container.handle_edit_event({
            'event': 'edit_event',
            'type': 'set_column_formula_edit',
            'step_id': get_new_step_id(),
            'sheet_index': 0,
            'column_header': 'A',
            'old_formula': '=0',
            'new_formula': '=1'
        })
    assert e_info.value.type_ == 'wrong_column_metatype_error'


def test_overwrites_step_valid():
    mito = create_mito_wrapper([1, 2, 3])
    mito.add_column(0, 'B')

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'edit_event',
        'type': 'add_column_edit',
        'step_id': mito.mito_widget.widget_state_container.curr_step['step_id'],
        'sheet_index': 0,
        'column_header': 'C',
    })

    wsc = mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.dfs[0].equals(pd.DataFrame(data={'A': [1, 2, 3], 'C': [0, 0, 0]}))


def test_failed_overwrite_rolls_back_to_previous_state():
    mito = create_mito_wrapper([1, 2, 3])
    mito.add_column(0, 'B')

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'edit_event',
        'type': 'add_column_edit',
        'step_id': mito.mito_widget.widget_state_container.curr_step['step_id'],
        'sheet_index': 1,
        'column_header': 'C',
    })

    wsc = mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.dfs[0].equals(pd.DataFrame(data={'A': [1, 2, 3], 'B': [0, 0, 0]}))


