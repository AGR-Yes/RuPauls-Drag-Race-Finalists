from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

placement = pd.read_csv("dash_data\placements.csv")
scores = pd.read_csv("dash_data\scores.csv")

app = Dash(__name__)


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
    dcc.Checklist(
        id="queen-dropdown",
        options=placement['queen'],
        value=["Americas", "Oceania"],
        inline=True
    ),
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
        hover_data=['score'])
    return fig


#---------------------------------------------------------------#
#Chart

episodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

melted = pd.melt(scores, id_vars='queen', value_vars=episodes)

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