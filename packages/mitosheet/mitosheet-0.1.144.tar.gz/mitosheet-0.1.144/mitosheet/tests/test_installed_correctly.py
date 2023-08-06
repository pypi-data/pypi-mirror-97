#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Tests some helper functions of local deployment.
"""

import pytest

from mitosheet.utils import get_app_directory_from_jupyter_lab_path_output


APP_DIR_TESTS = [
    (
        """Application directory:   /Users/nate/saga-vcs/monorepo/mito/venv/share/jupyter/lab
User Settings directory: /Users/nate/.jupyter/lab/user-settings
Workspaces directory: /Users/nate/.jupyter/lab/workspaces""",
        '/Users/nate/saga-vcs/monorepo/mito/venv/share/jupyter/lab'
    ),
    # Mac, with spaces
    (
        """Application directory:   /Users/nate/space dir/venv/share/jupyter/lab
User Settings directory: /Users/nate/.jupyter/lab/user-settings
Workspaces directory: /Users/nate/.jupyter/lab/workspaces""",
        '/Users/nate/space dir/venv/share/jupyter/lab'
    ),
    (
        """Application directory:   c:\\users\\nater\\mitovenv\\share\\jupyter\\lab
User Settings directory: C:\\Users\\nater\\.jupyter\\lab\\user-settings
Workspaces directory: C:\\Users\\nater\\.jupyter\\lab\\workspaces""",
        'c:\\users\\nater\\mitovenv\\share\\jupyter\\lab'
    ),
    (
        """Application directory:   c:\\users\\nater\\space folder\\mitovenv\\share\\jupyter\\lab
User Settings directory: C:\\Users\\nater\\.jupyter\\lab\\user-settings
Workspaces directory: C:\\Users\\nater\\.jupyter\\lab\\workspaces""",
        'c:\\users\\nater\\space folder\\mitovenv\\share\\jupyter\\lab'
    ),
]
@pytest.mark.parametrize('output, path', APP_DIR_TESTS)
def test_get_app_directory(output, path):
    assert get_app_directory_from_jupyter_lab_path_output(output) == path