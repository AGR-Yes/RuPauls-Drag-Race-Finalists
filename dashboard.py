import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# load data
df1 = pd.read_csv('dash_data/placements.csv')
#df2 = pd.read_csv('data_data/scores.csv')

# make plot

# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
# set app layout

html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('This is a paragraph.')
    ])
])



if __name__ == "__main__":
    app.run_server(debug=True)