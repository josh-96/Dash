import os
import numpy as np
import pandas as pd

import dash
from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import xgboost as xgb
from dash import html
import joblib

from .templates.kpi import generate_kpi

dash.register_page(__name__, path='/Prediction')

root_path = r'C:\Users\Josue\Documentos\Maestría\Aix-Marseille\SQL\Dash project\src\data\data.csv'

try:
    df = pd.read_csv(root_path)
except FileNotFoundError:
    print(f"Error! The file 'data.csv' was not found at the provided path: {root_path}")

# Convert 'BMI' column to numeric and replace non-numeric values with NaN
df['BMI'] = pd.to_numeric(df['BMI'], errors='coerce')

# Drop rows with missing values
df.dropna(inplace=True)

modelo_xgb = xgb.Booster()
modelo_xgb.load_model(r'C:\Users\Josue\Documentos\Maestría\Aix-Marseille\SQL\Dash project\src\models\xgb_model.json')

cols = ['BMI', 'HighChol', 'HeartDiseaseorAttack', 'PhysHlth', 'Sex']

# input1 = dcc.Input(id="BMI-textbox")
input1 = dcc.Input(
    id="BMI-textbox",
    placeholder="Enter BMI (12-98)",
    type="number",
    min=12,
    max=98
)
# input2 = dcc.RadioItems([0, 1], id='Sex-textbox', inline=True)
input2 = dcc.RadioItems(
    options=[
        {'label': 'Woman', 'value': 0},
        {'label': 'Man', 'value': 1}
    ],
    id='Sex-textbox',
    inline=True,
    style={'margin-center': '10px'}  # Adjust the margin as needed
)

# input3 = dcc.RadioItems([0, 1], id='HeartDiseaseorAttack-textbox', inline=True)
input3 = dcc.RadioItems(
    options=[
        {'label': 'No', 'value': 0},
        {'label': 'Yes', 'value': 1}
    ],
    id='HeartDiseaseorAttack-textbox',
    inline=True
)
# input4 = dcc.RadioItems([0, 1], id='HighChol-textbox', inline=True)
input4 = dcc.RadioItems(
    options=[
        {'label': 'No', 'value': 0},
        {'label': 'Yes', 'value': 1}
    ],
    id='HighChol-textbox',
    inline=True
)
input5 = dcc.Input(
    id="PhysHlth-textbox",
    placeholder="(0-30)",
    type="number",
    min=0,
    max=30
)


layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.H1('Predicting Diabetes'),
                html.Div(''),
            ]
        ),
        html.Form(
            className="row g-3 mb-3",
            children=[
                html.Div(
                    id='textboxes-container',
                    className="col-10",
                    children=[
                        html.Label("BMI"),
                        input1,
                        html.Br(),
                        html.Label("What is the Sex of your patient?"),
                        input2,
                        html.Label("Does your patient have history of Heart Disease or Attack ?"),
                        input3,
                        html.Label("Does your patient have High Cholesterol?"),
                        input4,
                        html.Label("How many days for the last month has your patient felt ill?"),
                        input5,

                    ]
                ),
                html.Button(
                    id='input-predict-go',
                    className='col-1 btn btn-primary',
                    n_clicks=0,
                    children='Predict',
                    type='button'
                )
            ]
        ),
        html.Div(
            id='output-predict-kpis',
            className="row",
        ),
    ]
)


@callback(
    Output(component_id='output-predict-kpis', component_property='children'),
    Input(component_id='input-predict-go', component_property='n_clicks'),
    State(component_id='Sex-textbox', component_property='value'),
    State(component_id='HighChol-textbox', component_property='value'),
    State(component_id='HeartDiseaseorAttack-textbox', component_property='value'),
    State(component_id='BMI-textbox', component_property='value'),
    State(component_id='PhysHlth-textbox', component_property='value')
)
def update_prediction(n_clicks, input_sex, input_highchol, input_heart, input_bmi, input_phys):
    if n_clicks > 0:
        input_data_dict = {
            "HighChol": [input_highchol],
            "BMI": [int(input_bmi)],
            "Sex": [input_sex],
            "HeartDiseaseorAttack": [input_heart],
            "PhysHlth": [int(input_phys)]
        }

        # Convert input data to DataFrame
        input_df = pd.DataFrame(input_data_dict)

        # Use DMatrix with enable_categorical=True
        dmatrix = xgb.DMatrix(input_df, enable_categorical=True)

        # Predict the probability of having diabetes
        y_prob = modelo_xgb.predict(dmatrix)

        # Set a threshold (you can adjust this threshold based on your preference)
        threshold = 0.5

        # Convert probability to binary prediction
        y_pred = 1 if y_prob > threshold else 0

        if y_pred == 1:
            prediction_message = "Your patient is likely to have Diabetes"
        else:
            prediction_message = "Your patient is unlikely to have Diabetes"

        kpi1 = generate_kpi(prediction_message, '')

        return kpi1
    else:
        raise PreventUpdate
