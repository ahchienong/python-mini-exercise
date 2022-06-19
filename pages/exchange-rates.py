from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
import json
import datetime
from utils.common import construct_url, call_thebank_api, prepare_df, generate_data_table, generate_exchange_rates_filters

dash.register_page(
    __name__, 
    path='/pages/exchange-rates',
    title='Exchange Rates',
    name='Exchange Rates'
)

# CONSTANTS
EXCHANGE_RATE = "https://api.bnm.gov.my/public/exchange-rate"

def generate_graph(id,title,data_frame):
    fig = px.bar(
            data_frame, 
            x="currency_code", 
            y="rate.middle_rate",
            hover_data=['rate.buying_rate', 'rate.selling_rate'],
            color="currency_code",
            barmode='group',
            title=title)
    
    # fig2 = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0, shared_xaxes=True)
    # trace = px.Scatter(x=data_frame._data["country_code"], 
    #             y=data_frame._data["rate.buying_rate"],
    #             marker=dict(color=colors[len(data)]),
    #             name=group)
    # fig.add_trace(trace)
    # fig.add_trace(px.line(data_frame, x="currency_code", y="rate.buying_rate"))
    # fig.add_trace(px.bar(x="currency_code", y="rate.selling_rate"))
    return dcc.Graph(
        id=id,
        figure=fig
    )

api_url = EXCHANGE_RATE
print(api_url)
_exchange_rates = call_thebank_api(api_url)
_exchange_rates_df = prepare_df(_exchange_rates)

def generate_exchange_rates():
    
    if _exchange_rates['data'] != []:
        _last_update = _exchange_rates['meta']['last_updated']
        # _exchange_rates_df = prepare_df(_exchange_rates)

        return html.Div(
        id='exchange_rates',
        children=[html.H3(children='Tabular Data'),
            html.P(children='last update: ' + _last_update, className='codes'),
            generate_data_table("exchange_rates-table",_exchange_rates_df),
            generate_graph("exchange_rates-graph", "Exchange Rates (latest)",_exchange_rates_df),
            html.Hr(),
            html.H6(children="Called API: " + api_url, className='codes'),
            html.Details([
                html.Summary('API Response', className='codes'),
                dcc.Markdown(
                    children='```\n'+json.dumps(_exchange_rates, indent=2)+'\n```'
                )
            ]),
        ])
    else:
        return html.Div(
        id='exchange_rates',
        children=[html.H3(children='Tabular Data'),
            html.H6(children="Called API: " + api_url, className='codes'),
            html.Details([
                html.Summary('API Response', className='codes'),
                dcc.Markdown(
                    children='```\n'+json.dumps(_exchange_rates, indent=2)+'\n```'
                )
            ]),
            html.Br(),
            html.Div(children='Data not available'),
            html.Hr()
        ])

@callback(
    Output('exchange_rates-graph', 'children'),
    Input('exchange_rates-table', 'derived_virtual_row_ids'),
    Input('exchange_rates-table', 'selected_row_ids'),
    Input('exchange_rates-table', 'active_cell'))
def update_graphs(row_ids, selected_row_ids, active_cell):
    selected_id_set = set(selected_row_ids or [])
    
    # print(_exchange_rates_df)
    
    if selected_row_ids is None:
        filtered_exchange_rates_df = _exchange_rates_df
    else:
        filtered_exchange_rates_df = {k:v for k,v in _exchange_rates_df.items() if k in selected_row_ids} 
    # print(filtered_exchange_rates_df)
        # filter(lambda i:i[0] in selected_id_set, _exchange_rates_df.iteritems())
        # {k:v for k,v in d.items() if k in included_keys}
    active_row_id = active_cell['row_id'] if active_cell else None

    # colors = ['#FF69B4' if id == active_row_id
    #           else '#7FDBFF' if id in selected_id_set
    #           else '#0074D9'
    #           for id in row_ids]

    return generate_graph("exchange_rates-graph", "Exchange Rates (latest)",filtered_exchange_rates_df)

    

layout = html.Div(children=[
    html.Br(),
    html.H1(children='Exchange Rates'),
    html.H6(children='Currency exchange rates from the Interbank Foreign Exchange Market in Kuala Lumpur. The price of selected countries currency in relation to Ringgit.'),
    # html.Br(),
    # generate_exchange_rates_filters(),
    html.Br(),
    generate_exchange_rates()
])