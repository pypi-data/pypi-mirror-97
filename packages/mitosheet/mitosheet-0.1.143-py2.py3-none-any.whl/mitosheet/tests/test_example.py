#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
import pytest

from mitosheet.save_utils import write_analysis
from mitosheet.example import MitoWidget, sheet
from mitosheet.utils import get_invalid_headers
from mitosheet.tests.test_utils import create_mito_wrapper_dfs

def test_example_creation_blank():
    df = pd.DataFrame()
    w = MitoWidget(df, tutorial_mode=False)

VALID_DATAFRAMES = [
    (pd.DataFrame()),
    (pd.DataFrame(data={'A': [1, 2, 3]})),
    (pd.DataFrame(data={'A0123': [1, 2, 3]})),
]
@pytest.mark.parametrize("df", VALID_DATAFRAMES)
def test_sheet_creates_valid_dataframe(df):
    mito = sheet(df)
    assert mito is not None

NON_VALID_HEADER_DATAFRAMES = [
    (pd.DataFrame(data={0: [1, 2, 3]}), ['0_']),
    (pd.DataFrame(data={0.1: [1, 2, 3]}), ['0_1_']),
    (pd.DataFrame(data={'A': [1, 2, 3], 0: [1, 2, 3]}), ['A', '0_']),
    (pd.DataFrame(data={'A': [1, 2, 3], '000': [1, 2, 3]}), ['A', '000_']),
    (pd.DataFrame(data={'A': [1, 2, 3], 'abc-123': [1, 2, 3]}), ['A', 'abc_123']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123': [1, 2, 3]}), ['A', '_123']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123_': [1, 2, 3]}), ['A', '_123_']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-abc_': [1, 2, 3]}), ['A', '_abc_']),
    (pd.DataFrame(data={'123': [1, 2, 3], '-abc_': [1, 2, 3]}), ['123_', '_abc_']),
    (pd.DataFrame(data={'ABC!DEF': [1, 2, 3], '123': [1, 2, 3]}), ['ABC_DEF', '123_']),
    (pd.DataFrame(data={'ABC?DEF': [1, 2, 3], '123': [1, 2, 3]}), ['ABC_DEF', '123_']),
    (pd.DataFrame(data={' ': [1, 2, 3], '123': [1, 2, 3]}), ['_', '123_']),
    (pd.DataFrame(data={'-': [1, 2, 3], ' !': [1, 2, 3]}), ['_', '__']),
    (pd.DataFrame(data={'##': [1, 2, 3], ' !': [1, 2, 3]}), ['numnum', '__']),
    (pd.DataFrame(data={'#!?5': [1, 2, 3], '#123': [1, 2, 3]}), ['num__5', 'num123']),
    (pd.DataFrame(data={'()': [1, 2, 3], '.,,': [1, 2, 3]}), ['__', '___']),
    (pd.DataFrame(data={'nate': [1, 2, 3], '.,,': [1, 2, 3]}), ['nate', '___']),
    (pd.DataFrame(data={'//': [1, 2, 3], '-': [1, 2, 3]}), ['__', '_']),
]

@pytest.mark.parametrize("df, new_keys", NON_VALID_HEADER_DATAFRAMES)
def test_sheet_errors_during_non_string_headers(df, new_keys):
    assert len(get_invalid_headers(df)) != 0
    mito = sheet(df)
    assert list(mito.widget_state_container.curr_step['dfs'][0].keys()) == new_keys

def test_create_with_multiple_dataframes():
    mito = sheet(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(data={'A': [1, 2, 3]}))
    assert mito is not None


def test_can_pass_saved_analysis_name():
    mito = create_mito_wrapper_dfs()
    mito.raw_python_import(
        "import pandas as pd\ndf = pd.DataFrame({'A': [1]})",
        ['df']
    )
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    mito = sheet(saved_analysis_name=analysis_name)
    assert len(mito.widget_state_container.dfs) == 1
    assert mito.widget_state_container.dfs[0].equals(
        pd.DataFrame({'A': [1]})
    )


def test_can_pass_analysis_saved_in_python():
    mito = sheet(saved_analysis_name='mito_simple_raw_import')
    assert len(mito.widget_state_container.dfs) == 1

def test_can_pass_saved_analysis_and_dataframes():
    df = pd.DataFrame({'A': [123]})
    mito = sheet(df, saved_analysis_name='mito_simple_raw_import')
    assert len(mito.widget_state_container.dfs) == 2

def test_errors_on_non_existing_analysis():
    with pytest.raises(ValueError):
        mito = sheet(saved_analysis_name='bork a dork')

def test_special_error_when_passing_filename():
    with pytest.raises(ValueError) as e_info:
        sheet('file.csv')
    assert 'use pandas' in e_info.value.args[0]



