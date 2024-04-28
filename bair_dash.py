import pandas as pd
import plotly.express  as px
import dash
from dash import dcc, html, dash_table
# from dash import html
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from scripts.sentiments import *

df = pd.read_csv(r'C:\Users\niyai\git\british-analysis\data\British_Airway_Review_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "British Airway Analysis"
server = app.server

app.layout = html.Div([
    html.Div(
##################################################### header
            id = "header-area",
            children=[
                html.P(),
                html.H1(
                    id = "header-title",
                    children = "British Airline Analysis",
                    style = {'textAlign' : 'center'}
                ),
                html.P(
                    id = "header-description",
                    children = ("Insights on Passenger Reviews and Traveller Experiences",
                              html.Br(), 
                              "(Nov 2015 - Aug 2023)"
                              ),
                    style = {'textAlign' : 'center'}
                ),
            ],
        ),
    html.P(),
    dcc.Tabs([
##################################################### first tab
        dcc.Tab(label = 'Analytics', 
    children=[
##################################################### filter 
        html.P(),
        html.Div(
            dbc.Row(
            id = "menu-area",
            children = [
                html.P(),
                dbc.Col(html.Div([
                    html.P(id = 'filter-date-name', children = ('Date Range')),
                    dcc.DatePickerRange(
                        id = "filter-date",
                        min_date_allowed = df.date.min().date(),
                        max_date_allowed = df.date.max().date(),
                        start_date = df.date.min().date(),
                        end_date = df.date.max().date(),
                        display_format = 'MMM YYYY'
                        )])
                        , width={'size' :3, 'offset': 1}),
                dbc.Col(html.Div([
                    html.P(id = 'filter-seat-name', children = ('Seat Type')),
                    dcc.Checklist(
                        id = "filter-seattype",
                        options = [{"label": seat_type, "value": seat_type} for seat_type in df.seat_type.unique()],
                        value = list(df.seat_type.unique())
                        )])
                        , width=2),
                dbc.Col(html.Div([
                    html.P(id = 'filter-traveller-name', children = ('Traveller Type')),
                    dcc.Checklist(
                        id = "filter-traveller",
                        options = [{"label": traveller, "value": traveller} for traveller in df.type_of_traveller.unique()],
                        value = list(df.type_of_traveller.unique()) 
                        )])
                        , width=2),
                dbc.Col(html.Div([
                   html.P(id = 'filter-verified-name', children = ('Verified Review')),
                    dcc.Checklist(
                        id = "filter-verified",
                        options = [{"label": verified, "value": verified} for verified in df.verified.unique()],
                        value = list(df.verified.unique())
                        )])
                        , width=2),
                dbc.Col(html.Div([
                   html.P(id = 'filter-recc-name', children = ('Recommend')),
                    dcc.Checklist(
                        id = "filter-recc",
                        options = [{"label": recommended, "value": recommended} for recommended in df.recommended.unique()],
                        value = list(df.recommended.unique())
                        )])
                        , width=2),
                html.P()
            ], style = {'textAlign' : 'center',
                        'font-size': '13px'
                        }
        )),
##################################################### organising visuals 
        html.P(),
        html.Div(
            id = "graph-container",
            children = 
            [   dbc.Row(
                        [dbc.Col(html.Div(dcc.Graph(id = "chart-reviews")), width = {'size': 5, 'offset': 1}),
                        dbc.Col(html.Div(dcc.Graph(id = "chart-recc")), width = {'size': 5})
                        ]),
                html.P()
            ]),
        html.P(),
        html.Div(
            id = "graph-container-2",
            children = 
            [   html.P("Distribution of Reviewers:", style = {'textAlign' : 'center','font-size': '18px', 'color' : 'white'}),
                dbc.Row(
                    [dbc.Col(html.Div(dcc.Graph(id = "chart-seattype")), width = {'size': 5, 'offset': 1}),
                    dbc.Col(html.Div(dcc.Graph(id = "chart-traveller")), width = 5),
                    ]),
                html.P(),
                dbc.Row(
                    [dbc.Col(html.Div(dcc.Graph(id = "chart-country")), width = {'size': 6, 'offset': 1}),
                    dbc.Col(html.Div(dcc.Graph(id = "chart-route")), width = 4),
                    ]),
                html.P(id = 'comment-nationality', style = {'textAlign' : 'center' ,'font-size': '14px', 'color' : 'white'}),
            ]
        )
    ]
    ), 
    dcc.Tab(
##################################################### second tab 
        label = 'WordCloud', 
        children = [
            html.P(),
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id = "chart-treemap", figure = fig_rw)), width = {'size': 10, 'offset': 1})
                ])
            ]),
    ])
])

def filter_data (start_date, end_date, seattype, traveller, verified, recc):
    df1 = df.loc[(df.date >= start_date) & (df.date <= end_date)] # date filter
    df2 = df1[df1['seat_type'].isin(seattype)] # seat type filter
    df3 = df2[df2['type_of_traveller'].isin(traveller)] # traveller type filter
    df4 = df3[df3['verified'].isin(verified)] # verified type filter
    df5 = df4[df4['recommended'].isin(recc)] # recommended type filter
    return df5

##################################################### callbacks
@app.callback(
    [Output("chart-recc", "figure"),
    Output("chart-reviews", "figure"),
    Output("chart-seattype", "figure"),
    Output("chart-traveller", "figure"),
    Output("chart-country", "figure"),
    Output("chart-route", "figure"),
    Output("comment-nationality", "children")
    ],
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)

    ######################### chart-recc
    recc = df_cleaned.groupby(['ym', 'recommended']).size().reset_index(name='count')
    fig_recc = px.line(recc, x = "ym", y = "count",
                       color = 'recommended',
                       color_discrete_map = {'No': 'red', 'Yes': 'green'}
                        )
    fig_recc.update_layout(hovermode="x",
                        title = "Recommendation Overtime",
                        title_x = 0.5,
                        yaxis_title = 'Number of Reviews',
                        xaxis_title = 'Date',
                        legend_title = None,
                        legend = dict(yanchor = "top", y = 0.98,
                                xanchor = "right", x = 0.99),
                        margin = dict(l = 50, r = 40, t = 50, b = 30)
                        )
    
    ######################### chart-reviews
    rev_num = df_cleaned.groupby(['ym', 'seat_type']).size().reset_index(name='count')
    fig_rev_num = px.bar(rev_num, x = "ym", y = "count",
                        color = 'seat_type',
                        color_discrete_map = {'Business Class': '#075AAA', 'Economy Class': '#A7A9AC',
                                              'First Class': '#B9CFED', 'Premium Economy' : '#01295C' }
                        )
    fig_rev_num.update_layout(hovermode="x",
                    title = "Exploring the Volume of Reviews",
                    title_x = 0.5,
                    yaxis_title = 'Number of Reviews',
                    xaxis_title = 'Date',
                    legend_title = None,
                    legend = dict(yanchor = "top", y = 0.98,
                              xanchor = "right", x = 0.99),
                    margin = dict(l = 50, r = 40, t = 50, b = 30)
                    )
    
    ######################### chart-seattype
    fig_seattype = px.pie(df_cleaned, 
                        names = "seat_type", 
                        color = "seat_type",
                        color_discrete_map = {'Business Class': '#075AAA', 'Economy Class': '#A7A9AC',
                                            'First Class': '#B9CFED', 'Premium Economy' : '#01295C' })
    fig_seattype.update_layout(title = "By Seat Type", 
                               title_x = 0.5,
                               margin = dict(l = 50, r = 40, t = 50, b = 30)
                               )
    
    ######################### chart-traveller
    # exploring if able to present in sunburst, where we can visualise % of yes and no in each category
    # fig_travellertype = px.sunburst(df_cleaned, 
                                # path = ['type_of_traveller','recommended'],
                                # color = 'recommended', 
                                # color_discrete_map = {'yes': 'green', 'no': 'red', '(?)' : 'royal blue'
                                #                     }
    fig_travellertype = px.pie(df_cleaned, 
                                names = 'type_of_traveller',
                                color = 'type_of_traveller',
                                color_discrete_map = 
                                    {'Couple Leisure': '#075AAA', 'Family Leisure': '#A7A9AC',
                                    'Solo Leisure': '#B9CFED', 'Business' : '#01295C' }
                            )
    fig_travellertype.update_layout(
                    title = "By Traveller Purpose",
                    title_x = 0.5,
                    margin = dict(l = 50, r = 40, t = 50, b = 30))
    
    ######################### chart-country
    df_country = df_cleaned.groupby(['country']).size().reset_index(name='count')
    df_c_index = df_country['count'].nlargest(10)
    top10_counts = df_country[df_country.index.isin(df_c_index.index)]
    fig_country = px.bar(top10_counts, x = 'country', y = 'count',
                            color = 'country',
                            color_discrete_sequence = px.colors.sequential.ice,
                            text_auto = True)
    fig_country.update_layout(hovermode="x",
                            title = "By Top 10 Countries",
                            title_x = 0.5,
                            yaxis_title = 'Number of Reviews',
                            xaxis_title = None,
                            xaxis = {'categoryorder':'total descending'},
                            showlegend = False,
                            margin = dict(l = 50, r = 40, t = 50, b = 30)
                            )
    fig_country.update_traces(textposition="outside")

    ######################### comment-nationality
    not_top10_counts = df_country[~df_country.index.isin(df_c_index.index)]
    
    ######################### chart-route
    fig_route = px.sunburst(df_cleaned, path = ['from','to'], color_discrete_sequence = px.colors.sequential.RdBu)
    fig_route.update_layout(title = "By Travel Routes",
                            title_x = 0.5,
                            margin = dict(l = 50, r = 40, t = 50, b = 30)
                            )
    fig_route.update_traces(textinfo = "label+percent parent")

    return fig_recc, fig_rev_num, fig_seattype, fig_travellertype, fig_country, fig_route, "there is a total of {} nationalities which are not in the top 10 and amounted to a count of {}".format(len(not_top10_counts.country.unique()), not_top10_counts['count'].sum())

if __name__ == "__main__":
    app.run_server(debug=True)
