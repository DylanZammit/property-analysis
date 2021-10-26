import plotly.express as px
from dash import html
from dash import dcc
import os
import pandas as pd
import numpy as np
import json
dirname = os.path.dirname(__file__)

df = pd.read_csv(os.path.join('data', 'remax_properties.csv'))

price_by_loc = df.groupby('locality').mean()['price']
locs = np.unique(df.locality)

fn = os.path.join('apps', 'geojson.json')

print('loading json...')
with open(fn) as f:
    out = json.load(f)

features = out['features']

mids = [x['id'] for x in features]
df = price_by_loc.loc[mids].reset_index()
ignore = ['Wardija']
df = df[~df.locality.isin(ignore)]

fig = px.choropleth(df, geojson=out, locations='locality', color='price',
                           color_continuous_scale="Turbo",
                           range_color=(min(df.price), max(df.price)),
                           labels={'price':'Price EUR'}
                          )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

layout = dcc.Graph(id='malta-graph', figure=fig, config={'displayModeBar': False, 'scrollZoom': False})

