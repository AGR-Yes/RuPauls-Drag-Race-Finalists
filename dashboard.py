from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


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
])


@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    df = pd.read_csv("dash_data\placements.csv")
    low, high = slider_range
    mask = (df['score'] > low) & (df['score'] < high)
    fig = px.scatter(
        df[mask], x="score", y="win", 
        color="w/r/e", size='score',
        hover_data=['score'])
    return fig


app.run_server(debug=True)