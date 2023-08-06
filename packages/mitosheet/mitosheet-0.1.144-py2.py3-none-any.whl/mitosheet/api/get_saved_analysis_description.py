from mitosheet.sheet_functions.types.utils import get_mito_type
from mitosheet.save_utils import read_analysis
from mitosheet.steps import STEP_TYPE_TO_STEP
import json


def get_saved_analysis_description(send, event, wsc):
    """
    Gets the description of the steps in the saved analysis, and sends
    it back to the frontend

    Sends '' if its unable to read in for any reason (or this analysis does)
    not exist.
    """
    analysis_name = event['analysis_name']
    analysis_steps = read_analysis(analysis_name)
    
    try:
        if analysis_steps is None:
            send({
                'event': 'api_response',
                'id': event['id'],
                'data': ''
            })
            return
        
        analysis_descriptions = []
        for step_number in analysis_steps['steps']:

            step = analysis_steps['steps'][step_number]
            STEP_OBJ = STEP_TYPE_TO_STEP[step['step_type']]

            # Create the step param object
            params = {key: value for key, value in step.items() if key in STEP_OBJ['params']}

            # Generate the step description
            step_description = STEP_OBJ['describe'](
                **params
            )

            analysis_descriptions.append({
                'step_type': step['step_type'],
                'step_description': step_description
            })

        send({
            'event': 'api_response',
            'id': event['id'],
            'data': json.dumps(analysis_descriptions)
        })
        
    except Exception as e:
        # As not being able to get the steps is not a critical failure, 
        # we return empty data if its not possible.
        send({
            'event': 'api_response',
            'id': event['id'],
            'data': ''
        })