import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

url = 'https://www.dhalia.com/buy/'
card_class = 'property-card--information'
property_request_url = 'https://laravel.dhalia.com:8000/server.php/api/property?propertyRef='
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

attributes = 'price region locality type bedrooms bathrooms type area'.split()
df = {k: [] for k in attributes}
s = requests.Session()

for j in range(1, 31):
    print(f'Page: {j}')
    r = s.get(url+f'?pageIndex={j}', headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    cards = soup.findAll('a', class_='propertybox')
    n = len(cards)
    for i, card in enumerate(cards):
        print(f'Card {i+1}', end='\r')

        reflink = card.find('span', class_='propertybox__ref-link').text
        rprop = s.get(property_request_url+reflink, headers=headers)
        content = BeautifulSoup(rprop.text, 'lxml').decode()
        data = json.loads(content[content.find('{'):content.rfind('}')+1])

        region = data['mapData']['mapFor']['region_keywords']
        property_details = data['propertyDetails']
        location = property_details['Location']
        price = property_details['Price']
        sqm = property_details['FArea']
        bedrooms = property_details['Bedrooms']
        bathrooms = property_details['Bathrooms']
        ptype = property_details['Type']

        df['price'].append(price)
        df['region'].append(region)
        df['locality'].append(location)
        df['type'].append(ptype)
        df['bedrooms'].append(bedrooms)
        df['bathrooms'].append(bathrooms)
        df['area'].append(bathrooms)

df = pd.DataFrame(df)
print(df)
print('Saving to csv')
df.to_csv('dhalia_properties.csv')
