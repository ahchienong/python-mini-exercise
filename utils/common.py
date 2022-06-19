
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

def generate_ref_rates_filters():
    return html.Div(
        id='filters',
        children=[  html.Div("Select Year",className="filters-item"), generate_year_dropdowns(),
                    html.Div("Select Month",className="filters-item"), generate_month_dropdowns()
        ],
        className="filters"
    )

def generate_exchange_rates_filters():
    return html.Div(
        id='filters',
        children=[  html.Div("Select Country",className="filters-item"), generate_country_dropdowns()
        ],
        className="filters"
    )

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

def generate_country_dropdowns():
    return dcc.Dropdown(
                options={
                'CHF': 'Swiss Franc',
                'CAD': 'Canadian Dollar',
                'BND': 'Bruneian Dollar',
                'AUD': 'Australian Dollar',
                'AED': 'UAE Dirham',
                'CNY': 'Chinese Yuan',
                'NPR': 'Nepalese Rupee',
                'VND': 'Vietnamese Dong',
                'USD': 'US Dollar',
                'TWD': 'Taiwan New Dollar',
                'THB': 'Thai Baht',
                'SGD': 'Singapore Dollar',
                'SAR': 'Saudi Arabian Riyal',
                'PKR': 'Pakistani Rupee',
                'PHP': 'Philippine Peso',
                'NZD': 'New Zealand Dollar',
                'MMK': 'Burmese Kyat',
                'KRW': 'South Korean Won',
                'KHR': 'Cambodian Riel',
                'JPY': 'Japanese Yen',
                'INR': 'Indian Rupee',
                'IDR': 'Indonesian Rupiah',
                'HKD': 'Hong Kong Dollar',
                'GBP': 'Great British Pound',
                'EUR': 'Euro',
                'EGP': 'Egyptian Pound',
                },
                value='USD',
                multi=True,
                id='country-dropdown',
                clearable=False,
                style=dict(
                    width='50%',
                    verticalAlign="middle"
                )
            )