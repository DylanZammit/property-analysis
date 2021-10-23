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
        dcc.Graph(id='price-by-area', style={'float': 'left','margin': 'auto', 'width':'60%'}, config={'displayModeBar': False}),
        html.Div([
            html.H2('Filters ', style={'padding': '20px', 'float': 'center','margin': 'auto', 'width': '100%',
                                       'text-align': 'center'}),
        html.Div([
        html.Div([
        html.Div('Locality ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
        dcc.Dropdown(id='loc-dd',
                     placeholder='Any',
                     multi=True,
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.locality)
                     ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                    )], className='filter-dd'),
        html.Div([
        html.Div('Region ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
        dcc.Dropdown(id='region-dd',
                     placeholder='Any',
                     multi=True,
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.region)
                     ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                    )], className='filter-dd'),
        html.Div([
        html.Div('# Bedrooms ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
        dcc.Dropdown(id='beds-dd',
                     placeholder='Any',
                     multi=True,
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.bedrooms)
                     ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                    )], className='filter-dd'),
        html.Div([
        html.Div('Property Type ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
        dcc.Dropdown(id='scatter-type-dd',
                     placeholder='Any',
                     multi=True, 
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.type)
                     ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                    )], className='filter-dd'),
        ], className='filters'),
        html.Table([
            html.Thead(html.Td('Property Information', colSpan='2')),
            html.Tr([html.Td('Locality', style={'width': '30%'}), html.Td(id='locality-output')]),
            html.Tr([html.Td('Region'), html.Td(id='region-output')]),
            html.Tr([html.Td('Price (EUR)'), html.Td(id='price-output')]),
            html.Tr([html.Td('# Rooms'), html.Td(id='rooms-output')]),
            html.Tr([html.Td('# Bedrooms'), html.Td(id='beds-output')]),
            html.Tr([html.Td('# Bathrooms'), html.Td(id='baths-output')]),
            html.Tr([html.Td(['Area (m', html.Sup(2), ')']), html.Td(id='area-output')]),
            html.Tr([html.Td(['Interior Area (m', html.Sup(2), ')']), html.Td(id='intarea-output')]),
            html.Tr([html.Td(['Exterior Area (m', html.Sup(2), ')']), html.Td(id='extarea-output')]),
            html.Tr([html.Td('Property Type'), html.Td(id='type-output')]),
        ]),
        html.Button('View Property', className='button', id='prop-link'),
        ], id='scatter-options')
        #dcc.Link(html.Button('View Property', style={'margin-top': '10px'}), id='prop-link', style={'margin-top': '10px'}, href=''),
    ], id='scatter-area', style={'overflow': 'hidden'}),
    html.Div([
    dcc.Dropdown(id='type-dd',
                 multi=True,
                 placeholder='All property types',
                 options=[
                     {'label': k, 'value': k} for k in np.unique(df.type)
                 ],
                 value=['Apartment']
                ),
        dcc.Graph(id='bar-by-type', config={'displayModeBar': False})], id='bar-area'),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display':'none'}),
])

