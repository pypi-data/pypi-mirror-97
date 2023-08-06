#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
The Mito package, which contains functions for creating a Mito sheet. 

To generate a new sheet, simply run:

import mitosheet
mitosheet.sheet()

If running mitosheet.sheet() just prints text that looks like `MitoWidget(...`, then you need to 
install the JupyterLab extension manager by running:

jupyter labextension install @jupyter-widgets/jupyterlab-manager@2;

Run this command in the terminal where you installed Mito. It should take 5-10 minutes to complete.

Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

NOTE: if you have any issues with installation, please email book a demo time at https://hubs.ly/H0FL1920
"""

import os
import pandas as pd
from mitosheet.example import MitoWidget, sheet
from mitosheet.errors import CreationError, EditError
from mitosheet._version import __version__, version_info

# Export all the sheet functions
from mitosheet.sheet_functions import *
# And the functions for changing types
from mitosheet.sheet_functions.types import *

from .nbextension import _jupyter_nbextension_paths


if __name__ == 'mitosheet':
    from mitosheet.user.user import initialize_user, is_local_deployment
    # Make sure the user is created and up to date, whenever mitosheet is imported
    initialize_user()

    from mitosheet.utils import is_imported_correctly

    # We check local deployment first, as this hopefully short curcits and saves us time
    if is_local_deployment() and not is_imported_correctly():
        print("It looks like Mito is incorrectly installed. To finish installing Mito, follow the documentation here: https://docs.trymito.io/")