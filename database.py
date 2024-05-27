import sqlite3
import asyncio
from offer_scraper import scrape_offers


def setup_database():
    connection = sqlite3.connect('vacation_hot_offers.db')
    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS offers''')

    cursor.execute('''CREATE TABLE offers (
                   agency_name TEXT,
                   offer_title TEXT,
                   offer_date TEXT,
                   offer_price TEXT
    )''')
    
    return connection, cursor


def populate_database(agency, cursor):
    agency_name, offers_titles, offers_dates, offers_prices = asyncio.run(scrape_offers(agency))
    for title, date, price in zip(offers_titles, offers_dates, offers_prices):
        cursor.execute('''INSERT INTO offers (agency_name, offer_title, offer_date, offer_price) VALUES (?, ?, ?, ?)''', (agency_name, title, date, price))


def query_database(agency):
    connection = sqlite3.connect('vacation_hot_offers.db')
    cursor = connection.cursor()
    
    # Populate the database with fresh data for the selected agency
    populate_database(agency, cursor)
    connection.commit()
    
    cursor.execute(
        "SELECT offer_title, offer_date, offer_price "
        "FROM offers "
        "WHERE agency_name = ?",
        (agency,)
    )
    records = cursor.fetchmany(6)
    connection.close()
    return records
