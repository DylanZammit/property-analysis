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
import os
from read_data import df

path = '/home/dylan/git/property-analysis'

layout = html.Div([
    html.Div([
        dcc.Tabs(id='analysis-tabs', className='tabs', value='malta-tab', children=[
            dcc.Tab(label='Locality prices', value='malta-tab'),
            dcc.Tab(label='Analysis', value='regression-tab')]),
        html.Div(id='analysis-content')
    ], id='scatter-area', style={'overflow': 'hidden'}),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display':'none'}),
])

