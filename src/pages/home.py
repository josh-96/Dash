import dash
from dash import dcc,html
from dash import dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc

from .templates.kpi import generate_kpi

dash.register_page(__name__, path='/Home')

# Home content
home_content = html.Div(
    className="row",
    children=[
        html.H1('Home',className='display-3'),
        html.Div('To be used by doctors'),
        generate_kpi('This model predicts the likelihood of having diabetes based on some medical data like BMI, Sex, History of heart disease and cholesterol and General Physical Health', "")
    ]
)

# BMI Calculator content
bmi_calculator_content = dbc.Container([
    dbc.Row(html.H1("BMI Calculator", className="display-5"), className="mb-4 mt-4"),
    dbc.Row([
        dbc.Col([
            html.Label("Weight (kg):"),
            dcc.Input(id="weight-input", type="number", value=70, step=1, min=1),
            html.Br(),
            html.Label("Height (m):"),
            dcc.Input(id="height-input", type="number", value=1.75, step=0.01, min=0.01),
            html.Br(),
            html.Button("Calculate BMI", id="calculate-button", n_clicks=0, className="btn btn-primary"),
        ], md=4),
        dbc.Col([
            html.Div(id="bmi-output", className="lead")
        ], md=8),
    ]),
])

# Combined layout
layout = html.Div([
    home_content,
    bmi_calculator_content
])


# Callback to update BMI result
@callback(
    Output("bmi-output", "children"),
    [Input("calculate-button", "n_clicks")],
    [dash.dependencies.State("weight-input", "value"),
     dash.dependencies.State("height-input", "value")]
)
def update_bmi(n_clicks, weight, height):
    if n_clicks > 0:
        try:
            bmi = weight / (height ** 2)
            return f"Your BMI is: {bmi:.2f}"
        except ZeroDivisionError:
            return "Error: Height should be greater than zero."
    else:
        return ""

