#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains an analysis with a single raw import step that imports
a single step into the sheet.
"""

MITO_SIMPLE_RAW_IMPORT_SAVE = {
    'name': 'mito_simple_raw_import',
    'saved_analysis': {
        "version": "0.1.96", 
        "steps": {
            "1": {
                "step_version": 1, 
                "step_type": "raw_python_import", 
                "python_code": "import pandas as pd\ndf = pd.DataFrame({'A': [123]})",
                "new_df_names": ["df"]
            }
        }
    }
}