# visit http://127.0.0.1:8050/ in your web browser.

import dash_daq as daq
from dash import html
from dash import dcc
import pandas as pd
import numpy as np
import os
from read_data import df

explanation = '''
The below graph shows how the price varies when the interior area of the property increases. Click a property (one of
the blue dots) to view more information. Filter your search based on your interest by choosing from the dropdowns on the
right. You can also click and drag to zoom on a specific area.
'''
layout = html.Div(id='regression-content', children=[
        #html.Div(explanation, id='reg-exp', className='instructions'),
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
        html.Div([
            #html.Div([
            #    daq.NumericInput(id='min-price', value=0, min=0, size='100px'),
            #    daq.NumericInput(id='max-price', value=1e7, min=0, size='100px'),
            #]),
            dcc.RangeSlider(id='price-range',
                min = 0, max = df.price.max(), value = [0, df.price.max()], step=5000,
                tooltip={"placement": "bottom", "always_visible": False},
                allowCross=False
                #updatemode='drag'
                ),
            html.Div(id='price-range-text'),
        ], className='filter-dd'),
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
