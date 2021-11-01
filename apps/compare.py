# visit http://127.0.0.1:8050/ in your web browser.

import dash_daq as daq
from dash import html
from dash import dcc
import pandas as pd
import numpy as np
import os
from read_data import df

layout = html.Div(id='compare-content', children=[

        dcc.Dropdown(id='compare-loc1-dd',
                     value='Sliema',
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.locality)
                     ]
                    ),
        dcc.Dropdown(id='compare-loc2-dd',
                     value='Qawra',
                     options=[
                         {'label': k, 'value': k} for k in np.unique(df.locality)
                     ]
                    ),
        dcc.Graph(id='compare-bar', config={'displayModeBar': False})
        ])
