# visit http://127.0.0.1:8050/ in your web browser.

from dash import html
from dash import dcc
import pandas as pd
import numpy as np
import os

###########################################
#df = pd.read_csv('/home/dylan/git/property-analysis/data/remax_properties.csv')
#df = pd.read_csv(os.path.join(os.pardir, 'data/remax_properties.csv'))
df = pd.read_csv(os.path.join('data', 'remax_properties.csv'))

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

layout = html.Div(id='regression-content', children=[
        dcc.Graph(id='price-by-area', style={'float': 'left','margin': 'auto', 'width':'60%'}, config={'displayModeBar': False}),
        html.Div([
            html.H2('Filters ', style={'padding': '20px', 'float': 'center','margin': 'auto', 'width': '100%',
                                       'text-align': 'center'}),
        html.Div([
        html.Div([
        html.Div('Locality ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
        dcc.Dropdown(id='loc-dd',
                     #placeholder='Any',
                     value=['Sliema'],
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
            html.Tr([html.Td('Price'), html.Td(id='price-output')]),
            html.Tr([html.Td('# Rooms'), html.Td(id='rooms-output')]),
            html.Tr([html.Td('# Bedrooms'), html.Td(id='beds-output')]),
            html.Tr([html.Td('# Bathrooms'), html.Td(id='baths-output')]),
            html.Tr([html.Td('Total Area'), html.Td(id='area-output')]),
            html.Tr([html.Td('Interior Area'), html.Td(id='intarea-output')]),
            html.Tr([html.Td('Exterior Area'), html.Td(id='extarea-output')]),
            html.Tr([html.Td('Property Type'), html.Td(id='type-output')]),
        ]),
        html.Button('View Property', className='button', id='prop-link'),
        ], id='scatter-options')
        #dcc.Link(html.Button('View Property', style={'margin-top': '10px'}), id='prop-link', style={'margin-top': '10px'}, href=''),
        ])
