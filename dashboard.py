import dash
from dash import Dash, dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

#---------------------------------------------------------------#
#DATAFRAMES DF DATASETS 

placement = pd.read_csv("dash_data/placements.csv")
scores = pd.read_csv("dash_data/scores.csv")
melted = pd.read_csv('dash_data/melted_scores.csv')

placement_col = ['bottom', 'low', 'safe', 'high', 'semiwin', 'win']

placement = placement.drop(columns=['Unnamed: 0'])

#---------------------------------------------------------------#
#Tables
#SCATTERPLOT TABLE
title = pd.DataFrame({
    "Letter": ["W", "R", "E"],
    "Title": ["Winner", "Runner Up", "Eliminated"],
    "Meaning": ["Queen won the season", "Queen was the runner up of the season", "Queen was eliminated during the finale"]
})

#LINECHART TABLE
linechart = pd.DataFrame({
    "Values":["0","1","2","3","4","5"],
    "Placement":["Bottom","Low","Safe","High","Semi-Win","Win"],
    "Meaning:":["Landed in bottom 2 and lipsynced",
                "Bad critiques, but was safe",
                "Safe in the episode",
                "Good critiques, but did not win the challenge",
                "Was in the top 2, but did not win the lipsync (All-Stars and select episodes)",
                "Won the episode; Or in All-Stars, won the top 2 lipsync"]
})

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

#CONTENT STYLE
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'backgroundColor':'#faeeeb',
}

#HEADER STYLE
HEADER_STYLE = {
    "textAlign":"center",
    "margin-bottom":"25px",
    'background-color': '#1f2630', 
    'text-align': 'center', 
    'padding': '4px'

}

#---------------------------------------------------------------#
#APP INITIALIZATION
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

#---------------------------------------------------------------#
#HEADER

header = html.Div([
    html.H1("You're a Winner, Baby!", style = HEADER_STYLE),
    html.H2("A RuPaul's Drag Race Dashboard for Finalists", style = HEADER_STYLE),
    ], className = "mt-4"
)

#---------------------------------------------------------------#
#FOOTER

footer = html.Div(
    html.A("Github", "https://github.com/agr-Yes/"), 
    style={'position': 'relative', 
           'bottom': 0, 
           'width': '100%', 
           'background-color': '#1f2630', 
           'text-align': 'center', 
           'padding': '5px'}
    )

#---------------------------------------------------------------#
#CONTENT
content = dbc.Container(
    [
#OPENING
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        """ 
"RuPaul's Drag Race" is a reality tv show casting talented drag queens every season to compete in challenges in attempt to make it to the top and be America's Next Drag Superstar and earn the cash prize.
            
Each episode consists of a main challenge and a themed runway show. Every week, one queen is declared the winner of an episode based on their performance, while two others are announced to be up for elimination. The bottom two must then compete to stay on the show with a lip-sync for their lives.

Expanding from the United States, the Drag Race franchises has reached out to other continents such as Europe and Asia; Making more queen declared as a 'Ru-girl' and potentially invited back to compete in an All-Star or International season.

This dashboard shows the data of the finalists in all franchises and countries (as of May 1, 2023). To see more, scroll down to see how your favorite finalist did!
                            """,
                            style = {"border": "1px",
                                     "padding": "10px",
                                     'whiteSpace': 'pre-wrap',
                                     }
                        ),
                    width = 9,
                ),
                dbc.Col(
                    html.Div([
                        html.H4("Contact me:"),
                        html.A("Instagram", href="https://www.instagram.com/ant0nreyes/"), html.Br(),
                        html.A("Github", href="https://github.com/AGR-Yes/"), html.Br(),
                        html.A("LinkedIn", href="https://www.linkedin.com/in/antongreyes/"), html.Br(),
                        html.H5("Project Repository"), html.Br(),
                        html.A("You're A Winner, Baby!", href="https://github.com/AGR-Yes/RuPauls-Drag-Race-Finalists"), html.Br(),
                        ]), style = {"border": "1px white solid",
                                     "padding": "10px",
                                     'whiteSpace': 'pre-wrap',
                                     },
                    width = 3,
                ),

            ],
            className="mt-4 mb-4",
        ),

#SCATTER PLOT 
        dbc.Row(
            [
                        html.H2('Score and Placement Scatter Plot', style = HEADER_STYLE),
                dbc.Col(
                    [

                        dcc.Graph(id="scatter-plot"),
                        
                    ], width = 7,
                ),

                dbc.Col(
                    [

                        html.P("Filter by placement:",
                               style={'font-weight': 'bold'},
                               className="mb-4"),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[{'label': col, 'value': col} for col in placement[placement_col]],
                            value = 'win',
                            className = 'dropdown2 mb-4',                            
                        ),
                        html.H4("Instructions:",
                               style={'font-weight': 'bold'},
                               className="mt-4"),
                        html.P(
                            """ 
Select from the dropdown list the placement you would want so see. 
The plot will adjust accordingly based on the placement selected. 
The scores show the score a contestant got by the end of their season. 
You can also click on the w/r/e on the graph's side, to show or hide specific placements.                               
                               """,
                               className="mt-4"), html.Br(),
                        html.P(
                            """
By hovering on each dot, you can find out which contestant it pertains to.                            
                        """),
                        dbc.Table([
                            html.Thead(html.Tr([html.Th(col) for col in title.columns])), 
                            html.Tbody([html.Tr([html.Td(title.iloc[i][col]) for col in title.columns]) for i in range(len(title))])   
                            ],
                            bordered=True,)                             

                    ], width = 5
                )
            ], className="mt-4 mb-4",
        ),

#LINECHART
        dbc.Row(
            [
                        html.H2('Final Progress per Finalist', style = HEADER_STYLE),
                        dcc.Graph(id="graph"),
                dbc.Col(
                    [
                        
                        html.P("Select the queens you want to compare",
                               style={'font-weight': 'bold'},
                               className="mt-4 mb-4"),
                        dcc.Dropdown(
                            id='queen-dropdown',
                            options=[{'label': queen, 'value': queen} for queen in melted['queen'].unique()],
                            value=['Sasha Colby'],
                            multi=True,
                            style={'width': '100%', 'margin': 'auto'},
                            className = 'dropdown1 mt-4',
                        ),
                        html.H4("Instructions:",
                               style={'font-weight': 'bold'},
                               className="mt-4"),
                        html.P(
                            """ 

Select from the dropdown list the queen you would want so see. 
This plot is capable of showing more than one queen at the same time, so just keep searching, adding, or removing as you want.
                               """,
                               className="mt-4"),
                        html.Br(),
                        html.P("""
In the y-axis, you can see the episodes from the lowest value (bottom placement) to the highest value possible (win placement). On the x-axis, you'll be able to see the number of episodes each contestant was a part of during their respective season. 

Since you can input multiple queens at the same time, you can compare multiple queens at the same time.
                        """),
                        
                    ], width = 7
                ),

                dbc.Col(
                    [

                        dbc.Table([
                            html.Thead(html.Tr([html.Th(col) for col in linechart.columns])), 
                            html.Tbody([html.Tr([html.Td(linechart.iloc[i][col]) for col in linechart.columns]) for i in range(len(linechart))])   
                            ],
                            bordered=True,
                            className="mt-4")  

                    ], width = 5
                ),

                        

            ], className="mt-4 mb-4",
        ),

#INFO TABLE
        dbc.Row(
            [           html.H2('Queen Placements', style = HEADER_STYLE),
                dbc.Col(
                    [
                        
                        html.H4("Instructions:",
                               style={'font-weight': 'bold'},
                               className=""),
                        html.P(
                            """ 
From the dropdown menu, select the finalist you want to view.
                               """,
                               className="mt-4"),
                        html.Br(),
                        html.P(
                            """ 
In the table, will see your selected Queen's season/s they were apart of, score, and number of placements they've accumulated during their run. 
Also, if you select a Queen that has been a part of multiple seasons (as long as they reached the finale,) you would see the score and placement count as well.
                               """,
                               className="mt-4"),

                    ], width = 5
                ),
                
                dbc.Col(
                    [

                        dcc.Dropdown(
                            id='row-dropdown',
                            options=[{'label': row['queen'], 'value': str(row.name)} for _, row in placement.iterrows()],
                            placeholder='Select a row...',
                            className = 'dropdown2 mb-4',
                        ),
                        dbc.Table(
                            [
                            html.Thead(
                                html.Tr([html.Th(col) for col in placement.columns])
                            ),
                            html.Tbody(id='table-body')],      
                            bordered=True,
                            dark=True,
                            hover=True,
                            responsive=True,
                            striped=True,
                        ),
                    ], width = 7
                ),

            ], className="mb-4",
        )
    ]
)

#---------------------------------------------------------------#
#APP LAYOUT
app.layout = html.Div([header, content, footer])

#---------------------------------------------------------------#
#APP CALLBACKS
#SCATTERPLOT
@app.callback(
    Output("scatter-plot", "figure"), 
    Input("dropdown", "value")
)
def update_bar_chart(dropdown_value):
    df = placement
    fig = px.scatter(
        df, x="score", y=dropdown_value, 
        color="w/r/e",
        hover_data=['queen'],
        template=dark_template,
        size = 'score')
    return fig

#LINECHART
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

#TABLE
@app.callback(
    Output('table-body', 'children'),
    [Input('row-dropdown', 'value')]
)
def update_table(selected_row):
    if selected_row is not None and selected_row != 'Unnamed: 0':
        queen_name = placement.loc[int(selected_row), 'queen']
        queen_rows = placement.loc[placement['queen'] == queen_name]
        return [
            html.Tr([
                html.Td(data) for data in queen_rows.iloc[i]
            ]) for i in range(len(queen_rows))
        ]
    else:
        return []

#---------------------------------------------------------------#
#RUN APP
app.run_server(debug=True)