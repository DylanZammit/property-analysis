import pdb
import plotly.express as px
import requests
import argparse
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
import csv
import time

locs = '''
Ħ'Attard
Ħal-Balzan
Bidnija
Birgu
Birkirkara
Birżebbuġa
Bormla
Ħad-Dingli
Fgura
Furjana
Ħal-Għargħur
Ħal-Għaxaq
Gudja
Gżira
Ħamrun
Iklin
Kalkara
Ħal-Kirkop
Ħal-Lija
Ħal-Luqa
Marsa
Marsaskala
Marsaxlokk
Imdina
Mellieħa
Imġarr
Mosta
Imqabba
Imsida
Imtarfa
In-Naxxar
Raħal-Ġdid
Pembroke
Tal-Pietà
Ħal-Qormi
Qrendi
Ir-Rabat,-Malta
Ħal-Safi
San-Ġwann
Santa-Luċija
Santa-Venera
Isla-(Senglea)
Is-Siġġiewi
Tas-Sliema
San-Ġiljan
San-Pawl-il-Baħar
Is-Swieqi
Ħal-Tarxien
Ta'-Xbiex
Belt-Valletta
Ix-Xgħajra
Ħaż-Żabbar
Ħaż-Żebbuġ
Iż-Żejtun
Iż-Żurrieq
Il-Fontana or It-Triq tal-Għajn
Għajnsielem
Għarb
Għasri
Ta-Kerċem
Munxar
Nadur
Qala
Rabat-Gozo
San-Lawrenz
Ta-Sannat
Xagħra
Xewkija
Iż-Żebbuġ (Gozo)
Marsalforn
'''.split()

url = 'https://nominatim.openstreetmap.org/search.php?city={}&country=malta&county={}&polygon_geojson=1&format=json'
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
s = requests.Session()

out_csv = '.csv'

ambig_map = {'Rabat': 'Northern', 'Mgarr': 'Northern', 'Zebbug': 'southern'}

df = pd.read_csv('data/remax_properties.csv')
if 0:
    type = 'Apartment'
    df = df[df.type==type]

price_by_loc = df.groupby('locality').mean()['price']
locs = np.unique(df.locality)

fn = 'geojson.json'
if not os.path.exists(fn):
    print('getting data...')

    features = []
    N = len(locs)
    print(f'Num localities = {N}')
    for i, loc in enumerate(locs):
        print(f'{i+1}/{N}: {loc}', end='')
        county, uloc = ('', loc) if loc not in ambig_map else (ambig_map[loc], loc)
        county, uloc = (tuple(loc.split(' - '))) if 'Gozo' in loc else (county, uloc)

        r = s.get(url.format(uloc, county), headers=headers)
        content = BeautifulSoup(r.text, 'lxml').decode()
        try:
            data = json.loads(content[content.find('{'):content.rfind('}')+1])

            my_loc = {'type': 'Feature',
                      'properties': {'locality': data['display_name']},
                      'geometry':  data['geojson'],
                      'lat': data['lat'],
                      'lon': data['lon'],
                      'id': loc}
            features.append(my_loc)
            my_loc = None
                                 
        except:
            print(f' ERROR #######')
            #import pdb; pdb.set_trace()
        else:
            print()

    out = {'features': features, 'type': 'FeatureCollection'}

    with open(fn, "w") as f:
        json.dump(out, f)

else:
    print('loading json...')
    with open(fn) as f:
        out = json.load(f)
    features = out['features']
