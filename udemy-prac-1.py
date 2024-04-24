#######
# Objective: Create a dashboard that takes in two or more
# input values and returns their product as the output.
######

# Perform imports here:
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input

# Launch the application:
app = dash.Dash(__name__)
server = app.server

# Create a Dash layout that contains input components
# and at least one output. Assign IDs to each component:

app.layout = html.Div([
    html.P(),
    dcc.RangeSlider(-10,10,1,
                    value = [-1,1],
                    id = 'rangeslider'
                    ),
    html.Div(id='multiply-output')
    ]
)

# Create a Dash callback:
@app.callback(
    Output('multiply-output', 'children'),
    [Input('rangeslider', 'value')])
def callback_a(wheels_value):
    final_output = wheels_value[0]*wheels_value[1]
    return '{}'.format(final_output)


# Add the server clause:
if __name__ == "__main__":
    app.run_server(debug=True)