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

path = '/home/dylan/git/property-analysis'
###########################################
df = pd.read_csv(os.path.join(path, 'data', 'remax_properties.csv'))

qtile = 0.99
qprice = df.price.quantile(qtile)
qintarea = df.int_area.quantile(qtile)
qarea = df.area.quantile(qtile)

n = len(df)

min_locs_by_type = 20
B = df.groupby('type').count()
types = B[B>=min_locs_by_type].dropna().index
df = df[df.type.isin(types)]
df = df[(df.price<qprice)&(df.int_area<qintarea)&(df.area<qarea)] # too much?
###########################################

layout = html.Div([
    html.Div([
        dcc.Tabs(id='analysis-tabs', value='malta-tab', children=[
            dcc.Tab(label='Locality prices', value='malta-tab'),
            dcc.Tab(label='Analysis', value='regression-tab')]),
        html.Div(id='analysis-content')
    ], id='scatter-area', style={'overflow': 'hidden'}),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display':'none'}),
])

