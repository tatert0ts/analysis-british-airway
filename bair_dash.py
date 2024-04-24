import pandas as pd
import plotly.express  as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

from wordcloud import WordCloud, STOPWORDS
import string

from test.sentiments import fig_word_tm
                # html.Div(dcc.Graph(figure = fig_word_tm)),

# to do: verified vs rating correlation?

df = pd.read_csv(r'C:\Users\niyai\git\british-analysis\British_Airway_Review_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = "slay"
server = app.server

# colors = {'coolblack' : '#01295C',
#           'persianblue' : '#075AAA',
#           'beaublue' : '#B9CFED',
#           'pigmentred' : '#EB2226',
#           'metallicsilver' : '#A7A9AC',
#           'notwhite' : '#EFE9E5'
#           }

# colors.get('coolblack')
# https://www.schemecolor.com/british-airways-website.php

text = " ".join(review for review in df.cleaned_reviews)
text = text.translate(str.maketrans('', '', string.punctuation))
stop_words = set(STOPWORDS)
stop_words.update(['ba', 'flight', 'flights', 'british', 'airway', 'airways'])
# Tokenize the text into words and remove empty strings
cleaned_words = [word for word in text.split() if word.strip()]
# convert into lowercase
# checking words against stopwords
cleaned_words = [word for word in cleaned_words if word.lower() not in stop_words]
word_freq = pd.Series(cleaned_words).value_counts()
df_word_freq = word_freq.reset_index()
df_word_freq.columns = ['Word', 'Frequency']
# Plot the treemap
fig_wordcloud = px.treemap(df_word_freq.head(50), path=['Word'], values='Frequency', title='Most Frequent Words')

app.layout = html.Div([
    html.Div(
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
                   html.P(id = 'filter-recc-name', children = ('Recommended')),
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
        ##################################################### visuals 
        html.P(),
        html.Div(
            id = "graph-container",
            children = 
            [   dbc.Row(dbc.Col(html.Div(dcc.Graph(id = "chart-reviews")), width = {'size': 10, 'offset': 1})),
                html.P(),
                # html.P("Review Ratings:", style = {'textAlign' : 'center','font-size': '18px', 'color' : 'white'}),
                # html.P(id = 'para-stars', style = {'textAlign' : 'center','font-size': '16px', 'color' : 'white'}),
                # dbc.Row(
                #     [dbc.Col(html.Div(dcc.Graph(id = "chart-stars")), width = {'size': 6, 'offset': 1}),
                #     dbc.Col(html.Div(dcc.Graph(id = "chart-stars-rec")), width = 4),
                #     ]),
            ]),
        html.P(),
        html.Div(
            id = "graph-container-2",
            children = 
            [   html.P("Distribution of Reviewers:", style = {'textAlign' : 'center','font-size': '18px', 'color' : 'white'}),
                dbc.Row(
                    [dbc.Col(html.Div(dcc.Graph(id = "seattype-chart")), width = {'size': 5, 'offset': 1}),
                    dbc.Col(html.Div(dcc.Graph(id = "traveller-chart")), width = 5),
                    ]),
                html.P(),
                # html.P("Demographics of Reviewers:", style = {'textAlign' : 'center','font-size': '18px', 'color' : 'white'}),
                dbc.Row(
                    [dbc.Col(html.Div(dcc.Graph(id = "country-chart")), width = {'size': 6, 'offset': 1}),
                    dbc.Col(html.Div(dcc.Graph(id = "route-chart")), width = 4),
                    ]),
            ]
        )
    ]
    ), # end of tab 1 
    dcc.Tab(label = 'Insights', 
            children = [
                html.P(children = [
                    '1. fig_rev_num - to note that there is a decreasing number of reviews as time passes, can attribute to datasets\' lack of upkeep - highest reviews in 2017, lowest in 2021 kiv when drawing conclusions from the rest of the dashboard.',
                       html.Br(), 
                       '3. fig_seattype - majority of the reviewers are from economy class, what is the rough % of seats available by seat type? does the proportion correspond?, hover tip to include number of customers, change the colour scheme',
                       html.P(),
                       '4. fig_travellertype - majority leisure, LEISURE vs BUSINESS -- are there any significant differences in ratings and sentiments???, hover tip to include number of customers, change the colour scheme',
                       html.P(),
                       '5. fig_country - countries with less thn 12.5 reviewers are categorised together under others, there are 47 unique countries, change details in the hover tip- consider top 10 only',
                       html.P(),
                       '7. fig_route - inconsistency with shortform and longhand'
                ], style = {'textAlign' : 'left','font-size': '14px', 'color' : 'white'}
                )
        ]),
    dcc.Tab(label = 'WordCloud', 
            children = [
                dbc.Col(html.Div(dcc.Graph(id = "chart-wordreviews", figure = fig_wordcloud)), width = {'size': 10, 'offset': 1})
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

@app.callback(
    Output("chart-reviews", "figure"),
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update_graph (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)
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
    return fig_rev_num

@app.callback(
    Output("seattype-chart", "figure"),
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update_graph (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)
    fig_seattype = px.pie(df_cleaned, names = "seat_type", color = "seat_type",
                color_discrete_map = {'Business Class': '#075AAA', 'Economy Class': '#A7A9AC',
                                      'First Class': '#B9CFED', 'Premium Economy' : '#01295C' })
    fig_seattype.update_layout(title = "By Seat Type", 
                               title_x = 0.5,
                               margin = dict(l = 50, r = 40, t = 50, b = 30)
                               )
    return fig_seattype

@app.callback(
    Output("traveller-chart", "figure"),
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update_graph (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)
    fig_travellertype = px.pie(df_cleaned, names = "type_of_traveller", color = 'type_of_traveller',
                            color_discrete_sequence = px.colors.sequential.RdBu
                            )
    fig_travellertype.update_layout(
                    title = "By Traveller Purpose",
                    title_x = 0.5,
                    margin = dict(l = 50, r = 40, t = 50, b = 30))
    return fig_travellertype


# len(min_cat.unique())

@app.callback(
    Output("country-chart", "figure"),
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update_graph (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)
    # Define the threshold for minority categories
    threshold = 2500*0.005 # bottom 0.5% anomalies
    # Count the frequency of each category
    country_counts = df_cleaned['country'].value_counts()
    # Identify categories below the threshold
    min_cat = country_counts[country_counts < threshold].index
    # Replace minority categories with 'Others'
    df_cleaned['new_country'] = df_cleaned['country'].where(~df_cleaned['country'].isin(min_cat), 'Others')
    fig_country = px.treemap(df_cleaned, path = ["new_country"], color = 'new_country', color_discrete_sequence = px.colors.sequential.RdBu
                             )
    fig_country.update_xaxes(categoryorder='total descending')
    fig_country.update_layout(
                    title = "By Nationality", title_x = 0.5,
                    margin = dict(l = 50, r = 40, t = 50, b = 30)
                    )
    return fig_country

@app.callback(
    Output("route-chart", "figure"),
    [Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-seattype", "value"),
    Input("filter-traveller", "value"),
    Input("filter-verified", "value"),
    Input("filter-recc", "value")
    ]
)
def update_graph (start_date, end_date, seattype, traveller, verified, recc):
    df_cleaned = filter_data(start_date, end_date, seattype, traveller, verified, recc)
    fig_route = px.sunburst(df_cleaned, path = ['from','to'], color_discrete_sequence = px.colors.sequential.RdBu)
    fig_route.update_layout(title = "By Travel Routes",
                            title_x = 0.5,
                            margin = dict(l = 50, r = 40, t = 50, b = 30)
                            )
    return fig_route

if __name__ == "__main__":
    app.run_server(debug=True)
