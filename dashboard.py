import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


#---------------------------------------------------------------#

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

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)

#---------------------------------------------------------------#


placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")
melted = pd.read_csv('dash_data\melted_scores.csv')


all_options = dict(zip(melted['code'], melted['queen']))




#---------------------------------------------------------------#
#Scatter plot
app.layout = html.Div([
    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by petal width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=4, max=41, step=5,
        marks={0: 'Low', 2.5: 'High'},
        value=[9, 29]
    ),
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph"),
    dcc.Dropdown(
        id="queen-dropdown",
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        placeholder="Select",
        multi = True, 
        searchable=True
    ),
    dcc.Dropdown(id="code-dropdown", multi=True, searchable=True, placeholder="Select"),
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
    dash.dependencies.Output('code-dropdown', 'options'),
    dash.dependencies.Input('queen-dropdown', 'value'))
def set_code_options(selected_indicator):
    if type(selected_indicator) == 'str':
        return [{'label': i, 'value': i} for i in all_options[selected_indicator]]
    else:
        return [{'label': i, 'value': i} for indicator in selected_indicator for i in all_options[indicator]]

app.run_server(debug=True)