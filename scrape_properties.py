import requests
import pandas as pd
from bs4 import BeautifulSoup

url='https://remax-malta.com/listings?Residential=true&Commercial=false&ForSale=true&ForRent=false&page=1'
base_dhalia = 'https://www.dhalia.com/'
url_dhalia = 'buy/'
card_class = 'property-card--information'

df = {'price': [], 'locality': [], 'type': [], 'bedrooms': []}
s = requests.Session()

for j in range(1, 31):
    print(f'Page {j}', end='\r')
    r = requests.get(base_dhalia+url_dhalia+f'?pageIndex={j}')
    soup = BeautifulSoup(r.text, 'lxml')

    cards = soup.findAll('a', class_='propertybox')
    n = len(cards)
    for i, card in enumerate(cards):
        price = card.find('span', class_='propertybox__price').text[3:]
        try:
            price = int(price.replace(',', ''))
        except:
            continue

        locality = card.find('h2').text
        property_type = card.find('h3').text
        bedrooms = card.find('div', class_='propertybox__footer').text[3:]

        df['price'].append(price)
        df['locality'].append(locality)
        df['type'].append(property_type)
        df['bedrooms'].append(bedrooms)

df = pd.DataFrame(df)
print(df)
print('Saving to csv')
df.to_csv('dhalia_properties.csv')
