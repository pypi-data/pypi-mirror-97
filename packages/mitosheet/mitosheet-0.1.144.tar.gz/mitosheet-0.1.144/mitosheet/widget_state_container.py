#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

from typing import List
import pandas as pd
import json
import uuid 


from mitosheet.steps.filter import execute_filter_column
from mitosheet.steps import EVENT_TYPE_TO_STEP, STEP_TYPE_TO_STEP
from mitosheet.updates import UPDATES
from mitosheet.steps.initial_steps.initalize import execute_initialize_step
from mitosheet.steps.initial_steps.initial_rename import execute_initial_rename_step
from mitosheet.utils import dfs_to_json
from mitosheet.transpiler.transpile import transpile
from mitosheet.user.user_utils import get_user_field


class WidgetStateContainer():
    """
    Holds the state of the steps, which represents operations that
    have been performed on the input dataframes. 
    """

    def __init__(self, dfs: pd.DataFrame):
        # Just in case they are a tuple, make them a list - as it's easier to operate with.
        # We also make a copy so we don't modify the original dataframes.
        dfs = [df.copy(deep=True) for df in dfs]

        # We also save a copy of the initial dataframe's keys, for easy access
        self.original_df_keys = [df.keys() for df in dfs]

        # For now, we just randomly generate analysis names. 
        # We append a UUID to note that this is not an analysis the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # We generate an initial rename step, which handles any issues with invalid headers
        # by converting them all to valid headers - which occurs before any formula step.
        dfs = execute_initial_rename_step(dfs)

        # Then we initialize the first initalize step
        self.steps = []
        execute_initialize_step(self, dfs)

        # We display the state that exists after the curr_step_idx is applied,
        # which means you can never see before the initalize step
        self.curr_step_idx = 0

    @property
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_idx]

    @property
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_idx]['dfs'])

    @property
    def dfs(self) -> List[pd.DataFrame]:
        return self.steps[self.curr_step_idx]['dfs']

    @property
    def df_names_json(self):
        """
        A JSON object containing the names of the dataframes
        """
        return json.dumps({'df_names': self.curr_step['df_names']})

    @property
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 

        NOTE: we only display the _first_ 2,000 rows of the dataframe
        for speed reasons. This results in way less data getting 
        passed around
        """
        return dfs_to_json(self.curr_step['dfs'])
    
    @property
    def df_shape_json(self):
        """
        Returns the df shape (rows, columns) of each dataframe in the 
        current step!
        """
        return json.dumps([
            {'rows': df.shape[0], 'cols': df.shape[1]}
            for df in self.curr_step['dfs']
        ])

    @property
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    @property
    def user_email(self):
        """
        Returns the user_email from user.json
        """
        return get_user_field('user_email')

    
    @property
    def step_data_list_json(self):
        """
        Returns a list of step data
        """
        step_data_list = []
        for index, step in enumerate(self.steps):
            STEP_OBJ = STEP_TYPE_TO_STEP[step['step_type']]
            params = {key: value for key, value in step.items() if key in STEP_OBJ['params']}
            step_data_list.append({
                'step_id': step['step_id'],
                'step_idx': index,
                'step_type': step['step_type'],
                'step_display_name': STEP_OBJ['step_display_name'],
                'step_description': STEP_OBJ['describe'](
                    df_names=step['df_names'],
                    **params,
                )
            })

        return json.dumps(step_data_list)

    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with a new step that was created
        by the edit_event. Each edit_event creates at most one step. 

        If there is an error in the creation of the new step, this
        function will delete the new, invalid step.
        """
        # NOTE: We ignore any edit if we are in a historical state, for now. This is a result
        # of the fact that we don't allow previous editing currently
        if self.curr_step_idx != len(self.steps) - 1:
            return

        try:
            curr_step = self.steps[-1]
            if self.curr_step['step_id'] == edit_event['step_id']:
                # If we are overwriting the event, then we set the current
                # step back 1 from the actual current step, so that we start
                # from the correct state
                curr_step = self.steps[-2]

            step_obj = EVENT_TYPE_TO_STEP[edit_event['type']]
            # Get the params for this event
            params = {key: value for key, value in edit_event.items() if key in step_obj['params']}

            # If it's filter, we need to do a lot of extra work
            # so we sent it into the execute function directly
            if step_obj['step_type'] == 'filter_column':
                execute_filter_column(
                    self,
                    **params
                )
                self.curr_step_idx = len(self.steps) - 1
                # If we made a new step, save the step id of this step
                if 'step_id' not in self.curr_step:
                    self.curr_step['step_id'] = edit_event['step_id']
                return 
            
            # Actually get the new step
            new_step = step_obj['execute'](curr_step, **params)

            # Save the parameters in the new step
            for key, value in params.items():
                new_step[key] = value
            
            # Furthermore, we save the step_id
            new_step['step_id'] = edit_event['step_id']

            # NOTE: no new errors occur below these lines, which is why we don't have to 
            # roll the back 

            # Finially, we append this step in the correct location to the steps
            if self.curr_step['step_id'] != edit_event['step_id']:
                self.steps.append(new_step)
            else:
                self.steps[-1] = new_step
            
            # and then update the index of the current step
            self.curr_step_idx = len(self.steps) - 1
        except:

            # We bubble the error up if it occurs
            # https://stackoverflow.com/questions/6593922/letting-an-exception-to-bubble-up
            raise


    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """
        for update in UPDATES:
            if update_event['type'] == update['event_type']:
                # Get the params for this event
                params = {key: value for key, value in update_event.items() if key in update['params']}
                # Actually execute this event
                update['execute'](self, **params)
                # And then return
                return

        raise Exception(f'{update_event} is not an update event!')        


    def _delete_curr_step(self):
        """
        Deletes the current step and rolls back a step!
        """
        self.steps.pop()

    


    