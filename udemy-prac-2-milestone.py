import pandas as pd
import plotly.express  as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from datetime import datetime

df = pd.read_csv(r'C:\Users\niyai\git\british-analysis\NaverStock.csv')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

app = dash.Dash(__name__)
tickers = df.Company.unique()

app.layout = html.Div([
    html.H1(id = 'header',
                children = 'Stock Ticker Dashboard',
                style = {'textAlign' : 'center', 'verticalAlign':'top'}
    ),
    html.Div([
        html.P('Select Start & End Dates:'),
        html.Div(
            [dcc.DatePickerRange(
            id = "filter-date",
            min_date_allowed = df.Date.min().date(),
            max_date_allowed = df.Date.max().date(),
            start_date = df.Date.min().date(),
            end_date = df.Date.max().date()
            )] , style = {'width': '30%', 'display': 'inline-block', 'paddingRight':'30px', 'verticalAlign':'top'}
            ),
        html.Div([
            html.P('Select Stock:'),
            html.Div(
                [dcc.Dropdown(
                id = "filter-dropdown",
                options = [{"label": Company, "value": Company} for Company in tickers],
                # placeholder = "Select a Stock",
                value = tickers[0],
                multi = True,
                searchable = True
                )]
                ),
            ], style = {'width': '30%', 'display': 'inline-block', 'paddingRight':'30px', 'verticalAlign':'top'}
            ),
        html.Div([
            html.Button('Submit', id='button-submit', n_clicks = 0)
            ], style = {'width': '30%', 'display': 'inline-block', 'paddingRight':'30px', 'verticalAlign':'top'}
            )
    ]),
    html.Div([
        # dcc.Graph(id = 'chart')
        # ], style = {'width': '80%', 'display': 'inline-block', 'paddingRight':'30px', 'verticalAlign':'top'}
        dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]}
        )
])
])

@app.callback(
    Output("chart", "figure"),
    [Input('button-submit', 'n_clicks')],
    [State("filter-dropdown", "value"),
    State("filter-date", "start_date"),
    State("filter-date", "end_date")
    ]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        # df = web.DataReader(tic,'iex',start,end)
        data = df.loc[(df.Date >= start_date) & (df.Date <= end_date) & (df.Company == tic)]
        traces.append({'x':data.Date, 'y': data.Close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
