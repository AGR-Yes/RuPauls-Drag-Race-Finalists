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
dark_template = {
    "layout": {
        "plot_bgcolor": "#1f2630",
        "paper_bgcolor": "#1f2630",
        "font": {"color": "#ffffff"}
    }
}

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
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

#---------------------------------------------------------------#
#HEADER



#---------------------------------------------------------------#
#GRAPHS PLOTS
content = dbc.Container(
    [
#opening text
        dbc.Row(
            [
                dbc.Col(
                    html.Div("Text column 1")
                ),
                dbc.Col(
                    html.Div("Text column 2")
                ),
                dbc.Col(
                    html.Div("Text column 3")
                )
            ],
            className="mt-4 mb-4",
        ),

        
        
#graph columns
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
                            value = 'win',
                            #className = 'btn-info mb-4',
                            style={'backgroundColor': 'black'}
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
                            style={'width': '100%', 'margin': 'auto'},
                            className = 'btn-info mb-4'
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
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"),
    Input("dropdown", "value")
)
def update_bar_chart(slider_range, dropdown_value):
    df = placement
    low, high = slider_range
    mask = (df[dropdown_value] > low) & (df[dropdown_value] < high)
    fig = px.scatter(
        df[mask], x="score", y=dropdown_value, 
        color="w/r/e",
        hover_data=['queen'],
        template=dark_template)
    return fig

@app.callback( #dropdown for slider
    Output('range-slider', 'value'),
    Input('dropdown', 'value')
)
def update_slider(placement_col):
    return [placement[placement_col].min(), placement[placement_col].max()]

@app.callback( #dropdown for line chart
    Output("graph", "figure"), 
    Input("queen-dropdown", "value"))
def update_line_chart(queens):
    df = melted
    mask = df.queen.isin(queens)
    fig = px.line(df[mask], 
        x="variable", y="value", color='queen',
        template=dark_template)
    return fig



#---------------------------------------------------------------#
#RUN APP
app.run_server(debug=True)