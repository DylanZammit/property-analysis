# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import webbrowser
import pdb
import numpy as np
import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

class App:

    wpage = None

    intro = 'Do you want to get a quote, or rough estimate of how much your property is worth in the current market in Malta? Or maybe do you want to do an in depth analysis on the current housing market? Press the options below to test out different stuff and try. Enjoy!'

    def __init__(self):
        app = dash.Dash(__name__)

        app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.H1('Property Analysis', style={'textAlign': 'center', 'font-size':'50px'}),
            html.Hr(),
            html.Div(self.intro, className='fade-in-text'),
            dcc.Link(html.Button('Get Quote', className='button-main-1'), href='/AAA', className='main-link'),
            dcc.Link(html.Button('Pro perty', className='button-main-2'), href='/BBB', className='main-link'),
            html.Div(id='page-content')
        ])

        self.app = app

        @app.callback(
            Output('page-content', 'children'),
            Input('url', 'pathname')
        )
        def button_click(pathname):
            return None
            #return html.H2(f'Hello {pathname}')

    def run_server(self, **kwargs):
        self.app.run_server(**kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-debug', action='store_true')
    args = parser.parse_args()

    debug = not args.no_debug

    app = App()
    app.run_server(debug=debug)
