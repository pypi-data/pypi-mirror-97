import io
import base64
import pandas as pd
from mitosheet.sheet_functions.types.utils import get_mito_type


def get_column_summary_graph(send, event, wsc):
    """
    Sends back a string representation of a PNG graph of the column_header 
    in the df at sheet_index in the widget state container.

    If the series is a numeric series, will return a histogram. Otherwise, as
    long as there are less than 20 distinct items in the series, will return
    a bar chart of the value count. Otherwise, will return nothing.
    """
    sheet_index = event['sheet_index']
    column_header = event['column_header']
    
    series: pd.Series = wsc.dfs[sheet_index][column_header]

    try:
        mito_type = get_mito_type(series)

        if mito_type == 'number_series':
            ax = series.plot.hist()
        else:
            if series.nunique() > 20:
                # Send an empty response
                send({
                    'event': 'api_response',
                    'id': event['id'],
                    'data': ''
                })
                # Then return so we only respond with an empty string
                return
            ax = series.value_counts().plot.bar()
        ax.set_title(column_header + ' frequencies')

        # From here: https://stackoverflow.com/questions/38061267/matplotlib-graphic-image-to-base64
        pic_IObytes = io.BytesIO()
        ax.figure.savefig(pic_IObytes,  format='png', transparent=True, bbox_inches='tight')
        pic_IObytes.seek(0)
        pic_hash = base64.b64encode(pic_IObytes.read()).decode("utf-8").replace("\n", "")

        send({
            'event': 'api_response',
            'id': event['id'],
            'data': pic_hash
        })
    except Exception as e:
        # As not being able to make a graph is a non-critical error that doesn't
        # result from user interaction, we don't want to throw an error if something
        # weird happens, so we just return nothing in this case
        send({
            'event': 'api_response',
            'id': event['id'],
            'data': ''
        })