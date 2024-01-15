import os


import dash
from dash import html
from dash import dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from .templates.kpi import generate_kpi

dash.register_page(__name__, path='/ExploratoryDataAnalysis')

df = pd.read_csv(r'C:\Users\Josue\Documentos\Maestría\Aix-Marseille\SQL\Dash project\src\data\data.csv')
df

cols = ['BMI', 'HighChol', 'HeartDiseaseorAttack', 'PhysHlth', 'Sex']


options = [
    {'label': col, 'value': col}
    for col in cols
]

dropdown1 = dcc.Dropdown(
    id='input-y',
    options=options,
    value='PhysHlth'  
)

dropdown2 = dcc.Dropdown(
    id='input-x',
    options=options,
    value='BMI' 
)


layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.H1('Exploratory Data Analysis'),
                html.Div(''),
            ]
        ),
        html.Form(
            className="row g-3 mb-3",
            children=[
                html.Div(
                    className="col-2",
                    children=[dropdown1],
                ),
                html.Div(
                    className="col-2",
                    children=[dropdown2],
                ),
                html.Button(
                    id='input-go',
                    className='col-1 btn btn-primary',
                    n_clicks=0,
                    children='Update',
                    type='button'
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-8",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                dcc.Graph(
                                    id='output-graph',
                                    # Set initial axis ranges based on the entire dataset
                                    config={'staticPlot': False},
                                    figure=px.scatter(df, x='BMI', y='PhysHlth').update_xaxes(range=[df['BMI'].min(), df['BMI'].max()]).update_yaxes(range=[df['PhysHlth'].min(), df['PhysHlth'].max()])
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="col-4",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                dcc.Graph(
                                    id='output-graph-hist',
                                    # Set initial axis range based on the entire dataset
                                    config={'staticPlot': False},
                                    figure=px.histogram(df, x='BMI', nbins=50).update_xaxes(range=[df['BMI'].min(), df['BMI'].max()])
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@callback(
    # Output(component_id='output-kpis', component_property='children'),
    Output(component_id='output-graph', component_property='figure'),
    Output(component_id='output-graph-hist', component_property='figure'),
    Input(component_id='input-go', component_property='n_clicks'),
    State(component_id='input-x', component_property='value'),
    State(component_id='input-y', component_property='value')
)


def update_graph(n_clicks, input_x, input_y):
    x_stats = df[input_x].describe()
    y_stats = df[input_y].describe()
    
    graph_ols = px.scatter(df, x=input_x, y=input_y)
    

    #  Set appropriate axis ranges based on the variable statistics
    graph_ols.update_xaxes(range=[x_stats['min'], x_stats['max']])
    graph_ols.update_yaxes(range=[y_stats['min'], y_stats['max']])

    graph_hist = px.histogram(df, x=input_x, nbins=50)

    return graph_ols, graph_hist
