# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import webbrowser
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

intro = 'Do you want to get a quote, or rough estimate of how much your property is worth in the current market in Malta? Or maybe do you want to do an in depth analysis on the current housing market? Press the options below to test out different stuff and try. Enjoy!'

layout = html.Div([
    html.H1('Property Analysis', style={'textAlign': 'center', 'font-size':'50px'}),
    html.Hr(),
    html.Div(intro, className='fade-in-text'),
    dcc.Link(html.Button('Get Quote', className='button-main-1'), href='/AAA', className='main-link'),
    dcc.Link(html.Button('Pro perty', className='button-main-2'), href='/BBB', className='main-link'),
    html.Br(),
], id='main-content')
