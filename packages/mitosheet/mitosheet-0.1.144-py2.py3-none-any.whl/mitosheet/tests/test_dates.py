#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
import pytest
import json

from mitosheet.tests.test_utils import create_mito_wrapper_dfs


def test_sheet_json_holds_dates_correctly():
    df = pd.DataFrame({
        'name': ['alice','bob','charlie'],
        'date_of_birth': ['2005-10-25','2002-10-2','2001-11-14']
    })

    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])

    mito = create_mito_wrapper_dfs(df)
    
    sheet_json = json.loads(mito.mito_widget.sheet_json)
    assert sheet_json[0]['data'][0][1] == '2005-10-25 00:00:00'
    assert sheet_json[0]['data'][1][1] == '2002-10-02 00:00:00'
    assert sheet_json[0]['data'][2][1] == '2001-11-14 00:00:00'
