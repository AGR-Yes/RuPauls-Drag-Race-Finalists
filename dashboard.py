import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)

#---------------------------------------------------------------#
#DATAFRAMES DF DATASETS 

placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")
melted = pd.read_csv('dash_data\melted_scores.csv')

episodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

options = [{'label': queen, 'value': queen} for queen in placement['queen'].unique()]

all_options = dict(zip(melted['code'], melted['queen']))

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

style = {'margin': "auto", "display": "block"}

#---------------------------------------------------------------#
#GRAPHS PLOTS
content = dbc.Container(
    [
        

    ]
)



html.Div([
    html.Div(
        id='main-content',
        style=CONTENT_STYLE),


    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot", style = style),
    html.P("Filter by petal width:"),
   
    

    dcc.RangeSlider(
        id='range-slider',
        min=4, max=41, step=5,
        marks={0: 'Low', 2.5: 'High'},
        value=[9, 29]),

    html.H4('Life expentancy progression of countries per continents'),
    
    dcc.Graph(id="graph", style = style),
    
    dcc.Checklist(
        id="queen-dropdown",
        options=melted['queen'].unique(),
        value=['Sasha Colby'],
        inline=True)
])

#---------------------------------------------------------------#
#APP LAYOUT
app.layout = html.Div([content])


#---------------------------------------------------------------#
#APP CALLBACKS

@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"), 
    [dash.dependencies.Input("range-slider", "value")])
def update_bar_chart(slider_range):
    df = placement
    low, high = slider_range
    mask = (df['score'] > low) & (df['score'] < high)
    fig = px.scatter(
        df[mask], x="score", y="win", 
        color="w/r/e", size='score',
        hover_data=['queen'])
    return fig

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