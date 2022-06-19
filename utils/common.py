
from dash import Dash, html, dcc, dash_table
import pandas as pd
import requests
import json

def construct_url(url,dict=""):
    if "".__eq__(dict):
        return url
    else:
        return url.format(list(dict.values())[0],list(dict.values())[1])

def call_thebank_api(url):
    HEADERS = { "Accept" : "application/vnd.BNM.API.v1+json" }
    response = requests.get(url, headers=HEADERS)
    return response.json()

def prepare_df(api_response):
    data_frame = pd.json_normalize(
        api_response, 
        record_path =['data']
    )
    #print(df)
    return data_frame

def generate_data_table(id,data_frame):
    dt = dash_table.DataTable(
        id=id,
        data = data_frame.to_dict('records'),
        columns = [{"name": i, "id": i} for i in data_frame.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_cell={
            'whiteSpace': 'normal',
            'textAlign': 'left'
        },
        virtualization=True,
        page_action='none')
    return dt

def generate_filters():
    return html.Div(
    id='filters',
    children=[  html.Div("Select Year",style={'margin-right': '2em'}), generate_year_dropdowns(),
                html.Div("Select Month",style={'margin-right': '2em'}), generate_month_dropdowns()],style=dict(display = 'flex'))
def generate_year_dropdowns():
    return dcc.Dropdown(
                options={
                '2020': '2020',
                '2021': '2021',
                '2022': '2022'
                },
                value='2022',
                id='year-dropdown',
                clearable=False,
                style=dict(
                    width='50%',
                    verticalAlign="middle"
                )
            )
def generate_month_dropdowns():
    return dcc.Dropdown(
                options={
                '1': 'January',
                '2': 'February',
                '3': 'March',
                '4': 'April',
                '5': 'May',
                '6': 'June',
                '7': 'July',
                '8': 'August',
                '9': 'Sept',
                '10': 'October',
                '11': 'November',
                '12': 'December',
                },
                value='6',
                id='month-dropdown',
                clearable=False,
                style=dict(
                    width='50%',
                    verticalAlign="middle"
                )
            )