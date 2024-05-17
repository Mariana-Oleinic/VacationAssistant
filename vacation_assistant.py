"""
Vacation Planner Assistant
"""


import tkinter as tk
from tkinter import font
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from offer_scraper import scrape_offers_and_populate_db
from convertor_scraper import scrape_currency_conversion


root = tk.Tk()
root.title("Vacation Planner Assistant")
root.eval("tk::PlaceWindow . center")
bold_font = font.Font(weight="bold")

IMAGE_PATH = "assets/BannerWebsite-with-logo-4.png"
image = Image.open(IMAGE_PATH)
width, height = 400, 200
resized_image = image.resize((width, height))
photo = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(root, image=photo)
image_label.pack(padx=10, pady=10)

# Code for "check offers" feature:
def query_db():
    """Query the database for offers"""
    agency = agency_var.get()
    scrape_offers_and_populate_db(agency)
    connection = sqlite3.connect('vacation_hot_offers.db')
    cursor = connection.cursor()
    cursor.execute(
    f"SELECT offer_title, offer_date, offer_price "
    f"FROM offers "
    f"WHERE agency_name = '{agency}'"
)
    records = cursor.fetchmany(6)
    connection.close()
    return records

def on_offers_check():
    """When clicking on "Check Offers" button, this function updates the  offers_result_label"""
    records = query_db()
    result = "List of Hot Offers 🔥:\n\n"
    result += "\n\n".join(" ".join(map(str, record)) for record in records)
    offers_result_label.config(text=result)

offers_label = tk.Label(root, text="Check vacation Hot Offers 🏝️:", font=bold_font)
offers_label.pack(pady=5)

agency_var = tk.StringVar()
agency_var.set("Admiral TUR")
agency_dropdown = tk.OptionMenu(root, agency_var, "Admiral TUR", "Panda TUR")
agency_dropdown.pack()

tk.Button(
    root,
    text="Check Offers",
    font=("System", 14),
    fg="violet",
    cursor='hand2',
    command=on_offers_check
).pack(pady=10)

offers_result_label = tk.Label(root, text="")
offers_result_label.pack(padx=20)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=20, pady=10)

# Code for "check budget" feature:
def on_budget_check():
    """When clicking on "Check Budget" button, this function updates the budget_result_label"""
    amount = amount_entry.get()
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    result = scrape_currency_conversion(amount, from_currency, to_currency)
    budget_result_label.config(text='Result: ' + result, font=bold_font)

budget_label = tk.Label(root, text="Check budget 💰:", font=bold_font)
budget_label.pack(pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack(padx=10)

from_currency_label = tk.Label(root, text="From Currency:")
from_currency_label.pack()
from_currency_var = tk.StringVar()
from_currency_var.set("MDL")
from_currency_dropdown = tk.OptionMenu(root, from_currency_var, "MDL", "USD", "EUR")
from_currency_dropdown.pack()

to_currency_label = tk.Label(root, text="To Currency:")
to_currency_label.pack()
to_currency_var = tk.StringVar()
to_currency_var.set("MDL")
to_currency_dropdown = tk.OptionMenu(root, to_currency_var, "MDL", "USD", "EUR")
to_currency_dropdown.pack()

tk.Button(
    root,
    text="Check Budget",
    font=("System", 14),
    fg="violet",
    cursor='hand2',
    command=on_budget_check,
).pack(pady=10)

budget_result_label = tk.Label(root, text="")
budget_result_label.pack(padx=20, pady=10)

root.mainloop()
