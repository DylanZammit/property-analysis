import pdb
import time
import requests
import argparse
import os
import pandas as pd
from bs4 import BeautifulSoup
import json
import csv
import time

parser = argparse.ArgumentParser()
parser.add_argument('-n', help='number of properties', default=500, type=int)
parser.add_argument('--debug', help='embed after request', action='store_true')
args = parser.parse_args()

nprops = args.n
take_pp = 1000
npages = nprops//take_pp+1
url = 'https://remax-malta.com/api/properties?Residential=true&Commercial=false&ForSale=true&ForRent=false&page={}&Take={}'
card_class = 'property-card--information'
property_request_url = 'https://laravel.dhalia.com:8000/server.php/api/property?propertyRef='
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
s = requests.Session()

property_url_base = 'https://remax-malta.com/listings/'

out_csv = 'remax_properties.csv'
attributes = 'price region locality locality_id type bedrooms bathrooms area int_area ext_area rooms webpage'.split()
df = {k: [] for k in attributes}

print(f'getting {nprops} requests...')

for page in range(1, int(npages)+1):
    print(f'Reading page {page}/{npages}...')
    time.sleep(3)
    take = take_pp if page < npages else nprops-page*take_pp
    if take < 10: continue

    r = s.get(url.format(page, take), headers=headers)
    content = BeautifulSoup(r.text, 'lxml').decode()
    #import pdb; pdb.set_trace()
    data = json.loads(content[content.find('{'):content.rfind('}')+1])['data']

    n_rejected = 0
    for prop in data['Properties']:
        if args.debug: pdb.set_trace()
        #if prop['Town'] == 'Gozo - Munxar': pdb.set_trace()
        if prop['TransactionType'] != 'For Sale' or prop['HidePriceFromWeb']: continue

        intarea = prop['TotalIntArea']
        extarea = prop['TotalExtArea']
        totarea = prop['TotalSqm']
        if intarea+extarea>totarea: totarea = intarea+extarea
        if intarea == 0: intarea = totarea-extarea
        if totarea == 0: totarea = intarea+extarea
        if extarea == 0: extarea = totarea-intarea
        if intarea+totarea+extarea==0: 
            print('Property {} has no area'.format(prop['MLS']))
            n_rejected+=1
            continue
        if totarea < 50: 
            print('Property {} area too small!'.format(prop['MLS']))
            n_rejected+=1
            continue
        if intarea==0:
            print('Property {} has no interior area!'.format(prop['MLS']))
            n_rejected+=1
            continue

        df['int_area'].append(intarea)
        df['ext_area'].append(extarea)
        df['area'].append(totarea)
        df['price'].append(prop['Price'])
        df['region'].append(prop['Province'])
        df['locality'].append(prop['Town'])
        df['locality_id'].append(prop['TownId'])
        df['type'].append(prop['PropertyType'])
        df['bedrooms'].append(prop['TotalBedrooms'])
        df['bathrooms'].append(prop['TotalBathrooms'])
        df['rooms'].append(prop['TotalRooms'])

        df['webpage'].append(os.path.join(property_url_base, prop['MLS']))
    print('done')

if not args.debug:
    with open(out_csv, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(attributes)

    df = pd.DataFrame(df)
    df.to_csv(out_csv, index=False, mode='a', header=False)
    print('='*30)
    print(f'Rejected {n_rejected} properties.')
    print(f'Saved {len(df)} properties to {out_csv} successfully!')
else:
    print(f'No saving in debug mode. {n_rejected} rejected.')
