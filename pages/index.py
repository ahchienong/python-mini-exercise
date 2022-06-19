import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, 
    path='/',
    title='Home Page',
    name='Home Page'
)

layout = html.Div(children=[
    html.H1(children='Welcome to Analytics'),

    html.Div(children='''
        Decision at your fingertips.
    '''),

])
