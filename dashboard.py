import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)
#---------------------------------------------------------------#
#STYLING
external_stylesheets = [
    {
        'href': 'file.css', 
        'rel':'stylesheet',
        'integrity':'sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor',
        'crossorigin':'anonymous'
     }
]


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#fdf9de",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'backgroundColor':'#faeeeb',
}

#---------------------------------------------------------------#
#SIDEBAR
sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

header_height, footer_height = "6rem", "10rem"
sidebar_width, adbar_width = "12rem", "12rem"

CONTENT_STYLE = {
    "margin-top": header_height,
    "margin-left": sidebar_width,
    "margin-right": adbar_width,
    "margin-bottom": footer_height,
    "padding": "1rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)
#---------------------------------------------------------------#
#MODAL
modal = html.Div(
    [
        dbc.Button("WHAT IS RCCE?", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("WHAT IS RCCE?")),
                dbc.ModalBody('Risk Communication and Community Engagement (RCCE) involves engaging and informing the public about risks in their community. This dashboard focuses on COVID-19 response and lists activities from January 2020 - June 2021.'),
                dbc.ModalBody('To begin, start by selecting an item on the sidebar!'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ],
    style = {
        'position':'fixed',
        'top':'2vh',
        'right':'2vw'
        }
)

#---------------------------------------------------------------#
#DATAFRAMES DF DATASETS 

placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")
melted = pd.read_csv('dash_data\melted_scores.csv')


all_options = dict(zip(melted['code'], melted['queen']))
#---------------------------------------------------------------#





#---------------------------------------------------------------#
#GRAPHS PLOTS
app.layout = html.Div([
    dcc.Location(id="url"),

    
    
    html.Div(
    id='main-content',
    style=CONTENT_STYLE),

    #content,
#SCATTERPLOT    
    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by petal width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=4, max=41, step=5,
        marks={0: 'Low', 2.5: 'High'},
        value=[9, 29]
),
#LINE CHART
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph",
              #style={'width': '90vh', 'height': '90vh'}
              ),
    dcc.Checklist(
        id="queen-dropdown",
        options=melted['queen'].unique(),
        value=['Sasha Colby'],
        inline=True
    ),
    modal,
    sidebar,
])


@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    df = placement
    low, high = slider_range
    mask = (df['score'] > low) & (df['score'] < high)
    fig = px.scatter(
        df[mask], x="score", y="win", 
        color="w/r/e", size='score',
        hover_data=['queen'])
    return fig


#---------------------------------------------------------------#
#Chart

episodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
#queen-dropdown
#code-dropdown

@app.callback(
    Output("graph", "figure"), 
    Input("queen-dropdown", "value"))
def update_line_chart(queens):
    df = melted
    mask = df.queen.isin(queens)
    fig = px.line(df[mask], 
        x="variable", y="value", color='queen')
    return fig

app.run_server(debug=True)