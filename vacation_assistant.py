"""
Vacation Planner Assistant
"""
import tkinter as tk
from tkinter import font
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import requests
from io import BytesIO
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

# Frame for the main content
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Left frame for offers
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky='nsew')

# Center frame for budget
center_frame = tk.Frame(main_frame)
center_frame.grid(row=0, column=2, sticky='nsew')

# Right frame for weather
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=4, sticky='nsew')

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.columnconfigure(4, weight=1)
main_frame.rowconfigure(0, weight=1)

# Separator between left and center frames
separator1 = ttk.Separator(main_frame, orient='vertical')
separator1.grid(row=0, column=1, sticky='ns', padx=5, pady=5)

# Separator between center and right frames
separator2 = ttk.Separator(main_frame, orient='vertical')
separator2.grid(row=0, column=3, sticky='ns', padx=5, pady=5)

# Code for "check offers" feature:
def query_db():
    """Query the database for offers"""
    agency = agency_var.get()
    scrape_offers_and_populate_db(agency)
    connection = sqlite3.connect('vacation_hot_offers.db')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT offer_title, offer_date, offer_price "
        "FROM offers "
        "WHERE agency_name = ?",
        (agency,)
    )
    records = cursor.fetchmany(6)
    connection.close()
    return records

def on_offers_check():
    """When clicking on "Check Offers" button, this function updates the offers_result_label"""
    records = query_db()
    result = "List of Hot Offers 🔥:\n\n"
    result += "\n\n".join(" ".join(map(str, record)) for record in records)
    offers_result_label.config(text=result)

def reset_offers():
    """Clear the offers result label"""
    offers_result_label.config(text="")

offers_label = tk.Label(left_frame, text="Check vacation Hot Offers 🏝️:", font=bold_font)
offers_label.pack(pady=5)

agency_var = tk.StringVar()
agency_var.set("Admiral TUR")
agency_dropdown = tk.OptionMenu(left_frame, agency_var, "Admiral TUR", "Panda TUR")
agency_dropdown.pack()

tk.Button(
    left_frame,
    text="Check Offers",
    font=("System", 14),
    fg="violet",
    cursor='hand2',
    command=on_offers_check
).pack(pady=10)

tk.Button(
    left_frame,
    text="Reset",
    font=("System", 14),
    fg="red",
    cursor='hand2',
    command=reset_offers
).pack(pady=5)

offers_result_label = tk.Label(left_frame, text="")
offers_result_label.pack(padx=20, pady=10)

# Code for "check budget" feature:
def on_budget_check():
    """When clicking on "Check Budget" button, this function updates the budget_result_label"""
    amount = amount_entry.get()
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    result = scrape_currency_conversion(amount, from_currency, to_currency)
    budget_result_label.config(text='Result: ' + result, font=bold_font)

def reset_budget():
    """Clear the budget result label"""
    budget_result_label.config(text="")
    amount_entry.delete(0, tk.END)

budget_label = tk.Label(center_frame, text="Check budget 💰:", font=bold_font)
budget_label.pack(pady=5)

amount_label = tk.Label(center_frame, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(center_frame)
amount_entry.pack(padx=10)

from_currency_label = tk.Label(center_frame, text="From Currency:")
from_currency_label.pack()
from_currency_var = tk.StringVar()
from_currency_var.set("MDL")
from_currency_dropdown = tk.OptionMenu(center_frame, from_currency_var, "MDL", "USD", "EUR")
from_currency_dropdown.pack()

to_currency_label = tk.Label(center_frame, text="To Currency:")
to_currency_label.pack()
to_currency_var = tk.StringVar()
to_currency_var.set("MDL")
to_currency_dropdown = tk.OptionMenu(center_frame, to_currency_var, "MDL", "USD", "EUR")
to_currency_dropdown.pack()

tk.Button(
    center_frame,
    text="Check Budget",
    font=("System", 14),
    fg="violet",
    cursor='hand2',
    command=on_budget_check,
).pack(pady=10)

tk.Button(
    center_frame,
    text="Reset",
    font=("System", 14),
    fg="red",
    cursor='hand2',
    command=reset_budget,
).pack(pady=5)

budget_result_label = tk.Label(center_frame, text="")
budget_result_label.pack(padx=20, pady=10)

# Code for "check weather" feature:
def fetch_weather_forecast(city, api_key, url):
    response = requests.get(url.format(city, api_key))
    data = response.json()
    if data["cod"] != "404":
        weather_data = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"] - 273.15),
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
        return weather_data
    else:
        return None
    
def on_weather_check():
    """When clicking on "Check Weather" button, this function updates the weather_result_label"""
    city = city_entry.get()
    api_key = open('API_KEY.txt', 'r').read()
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    weather_data = fetch_weather_forecast(city, api_key, current_weather_url)
    if weather_data:
        display_weather_forecast(weather_data)
    else:
        weather_result_label.config(text="City not found", font=bold_font)

def display_weather_forecast(weather_data):
    """Display weather forecast information"""
    global weather_frame
    # Destroy previous weather_frame if it exists
    if 'weather_frame' in globals():
        weather_frame.destroy()

    weather_frame = tk.Frame(right_frame)
    weather_frame.pack(pady=10)

    city_label = tk.Label(weather_frame, text=weather_data['city'], font=("Helvetica", 16))
    city_label.pack()

    temperature_label = tk.Label(weather_frame, text=f"{weather_data['temperature']}°C", font=("Helvetica", 48))
    temperature_label.pack()

    description_label = tk.Label(weather_frame, text=weather_data['description'], font=("Helvetica", 14))
    description_label.pack()

    # Fetch the weather icon
    icon_url = f"http://openweathermap.org/img/w/{weather_data['icon']}.png"
    response = requests.get(icon_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)

    icon_label = tk.Label(weather_frame, image=photo)
    icon_label.image = photo
    icon_label.pack()

def reset_weather():
    """Clear the weather result label, clear the city field, and destroy weather frame"""
    city_entry.delete(0, tk.END)
    global weather_frame
    weather_result_label.config(text="")
    if 'weather_frame' in globals():
        weather_frame.destroy()

weather_label = tk.Label(right_frame, text="Check weather forecast ⛅️:", font=bold_font)
weather_label.pack(pady=5)

city_label = tk.Label(right_frame, text="City:")
city_label.pack()
city_entry = tk.Entry(right_frame)
city_entry.pack(padx=10)

tk.Button(
    right_frame,
    text="Check Weather",
    font=("System", 14),
    fg="violet",
    cursor='hand2',
    command=on_weather_check
).pack(pady=10)

tk.Button(
    right_frame,
    text="Reset",
    font=("System", 14),
    fg="red",
    cursor='hand2',
    command=reset_weather,
).pack(pady=5)

weather_result_label = tk.Label(right_frame, text="")
weather_result_label.pack(padx=20, pady=10)

root.mainloop()
