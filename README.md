# Vacation Planner Assistant

This is a simple GUI application to assist users in planning their vacations. It provides features to check hot offers from two travel agencies, to convert currency amounts between three currencies, and to check weather forecast for a specified city or country.
The application uses **Tkinter** for the graphical user interface, **SQLite** for database management, and web scraping with **Beautiful Soup** and **Playwright** for data retrieval.
The project also includes testing with **Pytest** to ensure data integrity and code quality.

---

## Features
- **Check Vacation Hot Offers**: View a list of hot vacation offers from different agencies. Displays the offer title, date, and price for each offer.
- **Check Budget**: Convert an amount from one currency to another. Supports conversion between MDL, USD, and EUR currencies.
- **Check Weather**: View the current weather and weather forecast for a specified city or country. Displays the temperature in Celsius, a short weather description, and an icon representing the weather.

---

## Prerequisites
- **Python** should be installed on your PC.
- To use the weather forecast functionality in this application, you will need to obtain an **API key** from **OpenWeatherMap**. 

Follow these steps to get your Free API key:

1. Go to [OpenWeatherMap](https://openweathermap.org/).
2. Navigate to the "Pricing" section.
3. Scroll to the "Current weather and forecasts collection" table and click on "Get API key" under "Free" column.
4. You will be promted to create an account. Create an account (if you don't have one).
5. Once you sign in, go to the "My API keys" section, and copy your key.
6. This API key will be added into a file named API_KEY.txt. Further instructions will be provided in the next section below.

**Note:** Keep your API key secure and do not share it publicly. Treat it like a password.


---

## Installation 

1. Clone the repository:
```
git clone https://github.com/Mariana-Oleinic/VacationAssistant.git
```

2. Navigate to the project directory:
```
cd VacationAssistant
```
3. Create and activate a virtual environment:

For Mac/Linux:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
For Windows:
```
python -m venv venv
```
```
.\venv\Scripts\activate  
```
4. Install the required Python dependencies:

For Mac/Linux:
```
pip3 install -r requirements.txt 
```
For Windows:
```
pip install -r requirements.txt 
```
5. Install the necessary browser binaries for Playwright to function:

For Mac/Linux/Windows:
```
playwright install
```
6. Create API_KEY.txt file and add your API key there:

For Mac/Linux/Windows:
```
echo "PASTE_YOUR_API_KEY_HERE" >> API_KEY.txt
```
7. Run the application:

For Mac/Linux:
```
python3 vacation_assistant.py 
```
For Windows:
```
python vacation_assistant.py 
```

---

## Usage

1. Check Hot Offers:

- Select a travel agency from the dropdown menu.
- Click the "Check Offers" button to view the latest hot offers.

2. Check Budget:

- Enter the amount you want to convert.
- Select the source and target currencies from the dropdown menus.
- Click the "Check Budget" button to perform the currency conversion.

3. Check Weather:

- Enter the name of a city.
- Click the "Check Weather" button to view the current weather and the weather forecast for that city.

---

## Testing

1. Run the tests: 

For Mac/Linux/Windows:
```
pytest tests/
```
---
