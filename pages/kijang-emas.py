from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
import json
import datetime
from utils.common import construct_url, call_thebank_api, prepare_df, generate_data_table, generate_ref_rates_filters

dash.register_page(
    __name__, 
    path='/pages/kijang-emas',
    title='Kijang Emas',
    name='Kijang Emas'
)

# CONSTANTS
REF_RATE = "https://api.bnm.gov.my/public/kl-usd-reference-rate/year/{0}/month/{1}"
EXCHANGE_RATE = "https://api.bnm.gov.my/public/exchange-rate"
KIJANG_EMAS = "https://api.bnm.gov.my/public/kijang-emas"

current_time = datetime.datetime.now()

def generate_graph(id,title,data_frame):
    return dcc.Graph(
        id=id,
        figure=px.line(data_frame, x="date", y="rate", render_mode="svg",title=title)
    )

# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ],style={'textAlign': 'left', 'border-style': 'solid'})

def generate_ref_rates(options={}):
    if options=={}:
        options = {"year":current_time.year,"month":current_time.month}
    
    api_url = REF_RATE.format(list(options.values())[0],list(options.values())[1])
    print(api_url)
    _ref_rates = call_thebank_api(api_url)
    print(_ref_rates)
    if _ref_rates['data'] != []:
        _ref_rates_df = prepare_df(_ref_rates)

        return html.Div(
        id='ref_rates',
        children=[html.H3(children='Reference Rates'),
            html.H6(children="Called API: " + api_url),
            # html.Code(children=str(_ref_rates)),
            html.Details([
                html.Summary('API Response'),
                dcc.Markdown(
                    children='```\n'+json.dumps(_ref_rates, indent=2)+'\n```'
                )
            ]),
            html.Br(),
            generate_data_table("ref_rates-table",_ref_rates_df),
            generate_graph("ref_rates-graph", "Reference Rates (" + f'{options["year"]}' + " - " + f'{options["month"]}' + ")", _ref_rates_df),
            html.Hr()
        ])
    else:
        return html.Div(
        id='ref_rates',
        children=[html.H3(children='Reference Rates'),
            html.H6(children="Called API: " + api_url),
            # html.Code(children=str(_ref_rates)),
            html.Details([
                html.Summary('API Response'),
                dcc.Markdown(
                    children='```\n'+json.dumps(_ref_rates, indent=2)+'\n```'
                )
            ]),
            html.Br(),
            html.Div(children='Data not available'),
            html.Hr()
        ])
    
def generate_kijang_emas():
    _kijang_emas = call_thebank_api(KIJANG_EMAS)
    _kijang_emas_df = prepare_df(_kijang_emas)

    return html.Div(
    id='kijang_emas',
    children=[html.H3(children='Kijang Emas'),
        html.H6(children="Called API: " + KIJANG_EMAS),
        html.Details([
            html.Summary('API Response'),
            dcc.Markdown(
                children='```\n'+json.dumps(_kijang_emas_df, indent=2)+'\n```'
            )
        ]),
        html.Br(),
        # generate_dt(_kijang_emas_df),
        # generate_graph(_kijang_emas_df),
        html.Hr()
    ])
def generate_exchange_rates():
    _exchange_rates = call_thebank_api(EXCHANGE_RATE)
    _exchange_rates_df = prepare_df(_exchange_rates)

    return html.Div(
    id='exchange_rate',
    children=[html.H3(children='Exchange Rates'),
        html.H6(children="Called API: " + EXCHANGE_RATE),
        html.Details([
            html.Summary('API Response'),
            dcc.Markdown(
                children='```\n'+json.dumps(_exchange_rates, indent=2)+'\n```'
            )
        ]),
        html.Br(),
        # generate_dt(_exchange_rates_df),
        # generate_graph(_exchange_rates_df),
        html.Hr()
    ])

_kijang_emas = call_thebank_api(KIJANG_EMAS)
_exchange_rates = call_thebank_api(EXCHANGE_RATE)

@callback(
    Output("kijang_emas", component_property='children'),
    Input("year-dropdown", component_property='value'),
    Input("month-dropdown", component_property='value'),
    prevent_initial_call=True
)
def trigger_api(year_value,month_value):
    options = {"year":year_value,"month":month_value}
    return generate_ref_rates(options)

layout = html.Div(children=[
    html.H1(children='Kijang Emas'),
    html.Br(),
    generate_ref_rates_filters(),
    generate_ref_rates(),
    html.Br(),
    html.H3('--WIP--'),
    # generate_exchange_rate()
    html.H3(children='Exchange Rates: ('+EXCHANGE_RATE+')'),
    html.Code(children=str(_exchange_rates)),
    html.H3(children='Kijang Emas: ('+KIJANG_EMAS+')'),
    html.Code(children=str(_kijang_emas)),

])