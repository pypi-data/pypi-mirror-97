#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito
# Distributed under the terms of the Modified BSD License.

# TODO: do we need to update these to mito sheet?

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'mito',
        'require': 'mito/extension'
    }]