import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

#---------------------------------------------------------------#
#DATAFRAMES DF DATASETS 

placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")
melted = pd.read_csv('dash_data\melted_scores.csv')

placement_col = ['bottom', 'low', 'safe', 'high', 'semiwin', 'win']

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

#SIDEBAR STYLE
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#fdf9de",
}

#CONTENT STYLE
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'backgroundColor':'#faeeeb',
}

#---------------------------------------------------------------#
#APP INITIALIZATION
app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)

#---------------------------------------------------------------#
#HEADER



#---------------------------------------------------------------#
#GRAPHS PLOTS
content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('Interactive scatter plot with Iris dataset'),

                        dcc.Graph(id="scatter-plot"),

                        html.P("Filter by petal width:"),

                        dcc.Dropdown(
                            id='dropdown',
                            options=[{'label': col, 'value': col} for col in placement[placement_col]],
                            value = 'win'
                        ),

                        dcc.RangeSlider(
                            id='range-slider',
                            min=4, max=41, step=5,
                            marks={0: 'Low', 2.5: 'High'},
                            value=[9, 29]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.H4('Life expentancy progression of countries per continents'),

                        dcc.Graph(id="graph"),

                        dcc.Dropdown(
                            id='queen-dropdown',
                            options=[{'label': queen, 'value': queen} for queen in melted['queen'].unique()],
                            value=['Sasha Colby'],
                            multi=True,
                            style={'width': '100%', 'margin': 'auto'}
                        )
                    ]
                )
            ]
        )
    ]
)


#---------------------------------------------------------------#
#APP LAYOUT
app.layout = html.Div([content])

#---------------------------------------------------------------#
#APP CALLBACKS
@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"), 
    dash.dependencies.Input("range-slider", "value"))
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
    Output('range-slider', 'value'),
    Input('dropdown', 'value')
)
def update_slider(placement_col):
    return [placement[placement_col].min(), placement[placement_col].max()]

@app.callback(
    Output("graph", "figure"), 
    Input("queen-dropdown", "value"))
def update_line_chart(queens):
    df = melted
    mask = df.queen.isin(queens)
    fig = px.line(df[mask], 
        x="variable", y="value", color='queen')
    return fig



#---------------------------------------------------------------#
#RUN APP
app.run_server(debug=True)