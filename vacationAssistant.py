from tkinter import *
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
from offerScraper import scrape_offers_and_populate_db
from convertorScraper import scrape_currency_conversion


root = Tk()
root.title("Vacation Planner Assistant")
root.eval("tk::PlaceWindow . center")
bold_font = font.Font(weight="bold")

image_path = "assets/BannerWebsite-with-logo-4.png"
image = Image.open(image_path)
width, height = 400, 200  
resized_image = image.resize((width, height), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)
image_label = Label(root, image=photo)
image_label.pack(padx=10, pady=10)

# Code for "check offers" feature:
def query_db():
    agency = agency_var.get()
    scrape_offers_and_populate_db(agency) 
    connection = sqlite3.connect('vacation_hot_offers.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT offer_title, offer_date, offer_price FROM offers WHERE agency_name = '{agency}'")
    records = cursor.fetchmany(6)
    connection.close()
    return records

def on_offers_check():
    records = query_db()
    result = "List of Hot Offers 🔥:\n\n"
    result += "\n\n".join(" ".join(map(str, record)) for record in records)
    offers_result_label.config(text=result)   

offers_label = Label(root, text="Check vacation Hot Offers 🏝️:", font=bold_font)
offers_label.pack(pady=5)

agency_var = StringVar()
agency_var.set("Admiral TUR")  
agency_dropdown = OptionMenu(root, agency_var, "Admiral TUR", "Panda TUR")
agency_dropdown.pack()

Button(
    root,
    text="Check Offers",
    font=("System", 14),
    fg="violet",
    cursor='hand',
    command=on_offers_check
).pack(pady=10) 

offers_result_label = Label(root, text="")
offers_result_label.pack(padx=20) 

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=20, pady=10)

# Code for "check budget" feature:
def on_budget_check():
    amount = amount_entry.get()
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    result = scrape_currency_conversion(amount, from_currency, to_currency)
    budget_result_label.config(text='Result: ' + result, font=bold_font)

budget_label = Label(root, text="Check budget 💰:", font=bold_font)
budget_label.pack(pady=5)

amount_label = Label(root, text="Amount:")
amount_label.pack()
amount_entry = Entry(root)
amount_entry.pack(padx=10)

from_currency_label = Label(root, text="From Currency:")
from_currency_label.pack()
from_currency_var = StringVar()
from_currency_var.set("MDL")  
from_currency_dropdown = OptionMenu(root, from_currency_var, "MDL", "USD", "EUR")
from_currency_dropdown.pack()

to_currency_label = Label(root, text="To Currency:")
to_currency_label.pack()
to_currency_var = StringVar()
to_currency_var.set("MDL") 
to_currency_dropdown = OptionMenu(root, to_currency_var, "MDL", "USD", "EUR")
to_currency_dropdown.pack()

Button(
    root,
    text="Check Budget",
    font=("System", 14),
    fg="violet",
    cursor='hand',
    command=on_budget_check
).pack(pady=10) 

budget_result_label = Label(root, text="")
budget_result_label.pack(padx=20, pady=10)

root.mainloop()