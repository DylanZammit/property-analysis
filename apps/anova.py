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
        html.Div('Estimate Property Price', id='quote-title'),
        html.Div([
        html.Div(html.Img(src='assets/imdina.JPG', id='quote-image'), id='quote-image-container'),
        html.Div([
        html.Div([
            dcc.Dropdown(id='loc-quote-dd',
                         #placeholder='Choose locality',
                         value='Attard',
                         options=[
                             {'label': k, 'value': k} for k in np.unique(df.locality)
                         ]
                        )
        ], className='filter-quote-dd'),
        html.Div([
            dcc.Dropdown(id='type-quote-dd',
                         #placeholder='Choose property type',
                         value='Apartment',
                         options=[
                             {'label': k, 'value': k} for k in np.unique(df.type)
                         ]
                        )
        ], className='filter-quote-dd'),
        html.Div([
            dcc.Slider(id='beds-quote-slider',
                       min=1,
                       max=10,
                       marks={i: {'label': str(i)} for i in range(1, 11)},
                       #marks={i: {'label': str(i), 'color': '#77b0b1'} for i in range(1, 11)},
                       tooltip={"placement": "bottom", "always_visible": True},
                       step=1,
                       value=2,
                       updatemode='drag',
                       included=False),
            html.Div(id='beds-quote-output', className='slider-displayer')
        ], className='slider'),
        html.Div([
            dcc.Slider(id='area-quote-slider',
                       min=0,
                       max=500,
                       marks={i: {'label': str(i)+'m\u00b2'} for i in range(0, 501, 100)},
                       tooltip={"placement": "bottom", "always_visible": True},
                       step=5,
                       value=150,
                       updatemode='drag',
                       included=False),
            html.Div(id='area-quote-output', className='slider-displayer')
        ], className='slider'),
        ], id='quote-filter-area')], id='img-filters-quote'),
        #html.Button('Get Quote', className='button', id='quote-button'),
        html.Div(id='quote-output'),
], id='quote-area')
