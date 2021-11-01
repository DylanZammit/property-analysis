import pandas as pd
import numpy as np

df = pd.read_csv('data/remax_properties.csv')

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

region2loc = {}

for region in np.unique(df.region):
    A = df[df.region==region]
    region2loc[region] = np.unique(A.locality)

loc2region = {}
for loc in np.unique(df.locality):
    A = df[df.locality==loc]
    loc2region[loc] = A.iloc[0].region

region2img = {
    'Central': 'imdina.jpg',
    'Gozo': 'cittadella.jpg',
    'North': 'sea.jpg',
    'South': 'marsaxlokk.jpg',
    'Valletta': 'sea.jpg',
    'Sliema and St Julians Surroundings': 'imdina.jpg',
}
