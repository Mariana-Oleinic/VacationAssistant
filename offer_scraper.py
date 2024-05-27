import aiohttp
from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            return await response.text()
        else:
            raise ValueError(f"Failed to fetch data from {url}. Status code: {response.status}")


async def scrape_offers(agency):
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

    if agency not in agencies_data:
        raise ValueError(f"Agency '{agency}' is not supported.")
    
    url = agencies_data[agency]['url']
    
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
    
    soup = BeautifulSoup(result, 'html.parser')
    selectors = agencies_data[agency]['selectors']
    
    titles_data = soup.findAll(class_=selectors['offers'])
    offers_titles = [div.get_text(strip=True) for div in titles_data]
    
    dates_data = soup.findAll(class_=selectors['dates'])
    offers_dates = [div.get_text(strip=True) for div in dates_data]
    
    prices_data = soup.findAll(class_=selectors['prices'])
    offers_prices = [div.get_text(strip=True) for div in prices_data]
    
    agency_name = agency 

    return agency_name, offers_titles, offers_dates, offers_prices
