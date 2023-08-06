#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pandas as pd
import pytest
import json

from ..errors import EditError
from ..utils import get_column_filter_type
from .test_utils import create_mito_wrapper

COLUMN_FILTER_TYPE_TESTS = [
    ('int_column', 'number'),
    ('float_column', 'number'),
    ('mixed_float_and_int_column', 'number'),
    ('string_column', 'string'),
    ('mixed_string_and_int_column', 'string'),
]

@pytest.mark.parametrize('column_header, filter_type', COLUMN_FILTER_TYPE_TESTS)
def test_get_column_filter_type(column_header, filter_type):
    df = pd.DataFrame(data={
        'int_column': [1, 2, 3, 4, 5, 6],
        'float_column': [1.1, 2.2, 3.0, 4.5, 5.7, 6.9],
        'mixed_float_and_int_column': [1.1, 2, 3, 4, 5.7, 6.9],
        'string_column': ["1", "2", "3", "4", "5", "6"],
        'mixed_string_and_int_column': [1, 2, "3", 4, "5", "6"]
    })

    assert filter_type == get_column_filter_type(df[column_header])


def test_get_column_filter_type_after_formula():
    mito = create_mito_wrapper(['123'])
    mito.set_formula('=A', 0, 'B', add_column=True)
    assert 'string' == get_column_filter_type(mito.get_column(0, 'B', False))
    mito.set_formula('=100', 0, 'C', add_column=True)
    assert 'number' == get_column_filter_type(mito.get_column(0, 'C', False))