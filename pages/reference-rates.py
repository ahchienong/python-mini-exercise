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
    path='/pages/ref-rates',
    title='Reference Rates',
    name='Reference Rates'
)

# CONSTANTS
REF_RATE = "https://api.bnm.gov.my/public/kl-usd-reference-rate/year/{0}/month/{1}"

current_time = datetime.datetime.now()

def generate_graph(id,title,data_frame):
    return dcc.Graph(
        id=id,
        figure=px.line(data_frame, x="date", y="rate", render_mode="svg",title=title)
    )

def generate_ref_rates(options={}):
    if options=={}:
        options = {"year":current_time.year,"month":current_time.month}
    
    api_url = REF_RATE.format(list(options.values())[0],list(options.values())[1])
    print(api_url)
    _ref_rates = call_thebank_api(api_url)
    print(_ref_rates)
    if _ref_rates['data'] != []:
        _last_update = _ref_rates['meta']['last_updated']
        
        _ref_rates_df = prepare_df(_ref_rates)

        return html.Div(
        id='ref_rates',
        children=[
            html.H5(children='Tabular Data'),
            html.P(children='last update: ' + _last_update, className='codes'),
            generate_data_table("ref_rates-table",_ref_rates_df),
            generate_graph("ref_rates-graph", "Reference Rates (" + f'{options["year"]}' + " - " + f'{options["month"]}' + ")", _ref_rates_df),
            html.Hr(),
            html.H6(children="Called API: " + api_url, className='codes'),
            html.Details([
                html.Summary('API Response', className='codes'),
                dcc.Markdown(
                    children='```\n'+json.dumps(_ref_rates, indent=2)+'\n```'
                )
            ]),
        ])
    else:
        return html.Div(
        id='ref_rates',
        children=[html.H3(children='Tabular Data'),
            html.H6(children="Called API: " + api_url),
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

@callback(
    Output("ref_rates", component_property='children'),
    Input("year-dropdown", component_property='value'),
    Input("month-dropdown", component_property='value'),
    prevent_initial_call=True
)
def trigger_api(year_value,month_value):
    options = {"year":year_value,"month":month_value}
    return generate_ref_rates(options)

layout = html.Div(children=[
    html.Br(),
    html.H1(children='Kuala Lumpur USD/MYR Reference Rate'),
    html.H6(children='A reference rate that is computed based on weighted average volume of the interbank USD/MYR FX spot rate transacted by the domestic financial institutions and published daily at 3:30 p.m.'),
    html.Br(),
    generate_ref_rates_filters(),
    html.Br(),
    generate_ref_rates()
])