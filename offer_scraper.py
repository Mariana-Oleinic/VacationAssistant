import requests
from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect('vacation_hot_offers.db')
cursor = connection.cursor()

cursor.execute('''DROP TABLE IF EXISTS offers''')

cursor.execute('''CREATE TABLE offers (
               agency_name TEXT,
               offer_title TEXT,
               offer_date TEXT,
               offer_price TEXT
)''')

def scrape_offers_and_populate_db(agency):
    agencies_data = {
        'Admiral TUR': {
            'url': 'https://admiral.travel/en',
            'selectors': {
                'offers': 'select_tur_item_bar',
                'dates': 'select_tur_item_info_incluse_transport',
                'prices': 'select_tur_item_price_item'
            }
        },
        'Panda TUR': {
            'url': 'https://pandatur.md/en',
            'selectors': {
                'offers': 'hot_offer_item_region_name',
                'dates': 'hot_offer_item_date',
                'prices': 'hot_offer_item_region_price'
            }
        }
    }

    if agency in agencies_data:
        url = agencies_data[agency]['url']
        response = requests.get(url)
        if response.status_code == 200:
            result = response.text
            soup = BeautifulSoup(result, 'html.parser')
            selectors = agencies_data[agency]['selectors']
            
            titles_data = soup.findAll(class_=selectors['offers'])
            offers_titles = [div.get_text(strip=True) for div in titles_data]
            
            dates_data = soup.findAll(class_=selectors['dates'])
            offers_dates = [div.get_text(strip=True) for div in dates_data]
            
            prices_data = soup.findAll(class_=selectors['prices'])
            offers_prices = [div.get_text(strip=True) for div in prices_data]

            agency_name = agency

            for title, date, price in zip(offers_titles, offers_dates, offers_prices): 
                cursor.execute('''INSERT INTO offers (agency_name, offer_title, offer_date, offer_price) VALUES (?, ?, ?, ?)''', (agency_name, title, date, price))

        connection.commit()

