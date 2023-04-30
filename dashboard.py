import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


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

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
#---------------------------------------------------------------#
#SIDEBAR
sidebar = html.Div([
    html.H2("Sidebar"),
    html.Hr(),
    html.P("A simple sidebar layout with navigation links", className="lead"),
    dbc.Nav([
            #dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
            #dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
            #dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
        ], vertical=True, pills=True,
    )],
    style=SIDEBAR_STYLE
)
#---------------------------------------------------------------#


#---------------------------------------------------------------#
#DATAFRAMES DF DATASETS 

placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")
melted = pd.read_csv('dash_data\melted_scores.csv')

episodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

all_options = dict(zip(melted['code'], melted['queen']))
#---------------------------------------------------------------#


graphstyle ={'width': '70vw',
        'height': '70vh',
        'margin': 'auto',
        'display': 'block'}

#---------------------------------------------------------------#
#GRAPHS PLOTS
content = html.Div([
#SCATTERPLOT    


    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot",
              responsive='auto',
              style=graphstyle),
    html.P("Filter by petal width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=4, max=41, step=5,
        marks={0: 'Low', 2.5: 'High'},
        value=[9, 29],
        verticalHeight=900,
        ),


#LINE CHART
    
    
html.Div(
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph",
              responsive='auto',
              style=graphstyle),
    dcc.Checklist(
        id="queen-dropdown",
        options=melted['queen'].unique(),
        value=['Sasha Colby'],
        inline=True,
        ),
    sidebar,
)
])



#---------------------------------------------------------------#
#APP LAYOUT
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


#---------------------------------------------------------------#
#CALLBACK
#SCATTERPLOT
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

#LINE GRAPH
@app.callback(
    Output("graph", "figure"), 
    Input("queen-dropdown", "value"))
def update_line_chart(queens):
    df = melted
    #mask = df.queen.isin(queens)
    fig = px.line(df[df.queen.isin(queens)], 
        x="variable", y="value", color='queen')
    return fig



#---------------------------------------------------------------#
#RUN APP
app.run_server(debug=True)