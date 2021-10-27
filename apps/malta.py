import plotly.express as px
from dash import html
from dash import dcc
import os
import pandas as pd
import numpy as np
import json

token = 'pk.eyJ1IjoiZHlsYW56YW0iLCJhIjoiY2t2OWcxaWt3NXV4dzJvczc3cm45YTlrcCJ9.k-EnkUZMK1rybum84KDgXw'
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
#df.at[0, 'price'] = 0
import plotly.graph_objects as go

lat, lon = 35.917973, 14.409943
fig = go.Figure(go.Choroplethmapbox(geojson=out, locations=df.locality, z=df.price, colorscale='Turbo',
                                    zmin=min(df.price), zmax=max(df.price), marker_line_width=0.1))
fig.update_layout(mapbox_style="light", mapbox_zoom=10, mapbox_accesstoken=token, mapbox_center = {"lat": lat,
                                                                                                   "lon": lon})
#fig.update_layout(mapbox_style="light", mapbox_accesstoken=token, mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})

#fig = px.choropleth(df, geojson=out, locations='locality', color='price',
#                           color_continuous_scale="Turbo",
#                           range_color=(min(df.price), max(df.price)),
#                           labels={'price':'Price EUR'}
#                          )
#fig.update_geos(fitbounds="locations", visible=False)
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

layout = dcc.Graph(id='malta-graph', figure=fig, config={'displayModeBar': False})
#layout = dcc.Graph(id='malta-graph', figure=fig, config={'displayModeBar': False, 'scrollZoom': False})

