import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import csv
import time

nprops = 5000
url = 'https://remax-malta.com/api/properties?Residential=true&Commercial=false&ForSale=true&ForRent=false&page=1&Take={}'.format(nprops)
card_class = 'property-card--information'
property_request_url = 'https://laravel.dhalia.com:8000/server.php/api/property?propertyRef='
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
s = requests.Session()

out_csv = 'remax_properties.csv'
attributes = 'price region locality type bedrooms bathrooms area rooms'.split()
with open(out_csv, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(attributes)

print('getting request...')
r = s.get(url, headers=headers)
content = BeautifulSoup(r.text, 'lxml').decode()
data = json.loads(content[content.find('{'):content.rfind('}')+1])['data']

df = {k: [] for k in attributes}
for prop in data['Properties']:
    print(prop['Coordinates'], end='\r')

    if prop['TransactionType'] != 'For Sale' or prop['HidePriceFromWeb']:
            continue
    df['price'].append(prop['Price'])
    df['region'].append(prop['Province'])
    df['locality'].append(prop['Town'])
    df['type'].append(prop['PropertyType'])
    df['bedrooms'].append(prop['TotalBedrooms'])
    df['bathrooms'].append(prop['TotalBathrooms'])
    df['rooms'].append(prop['TotalRooms'])
    df['area'].append(prop['TotalSqm'])

df = pd.DataFrame(df)
df.to_csv(out_csv, index=False, mode='a', header=False)
