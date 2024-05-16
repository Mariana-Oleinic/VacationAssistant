# Vacation Planner Assistant

This is a simple GUI application to assist users in planning their vacations. It provides features to check hot offers from two travel agencies and to convert currency amounts between three currencies.
The application uses **Tkinter** for the graphical user interface, **SQLite** for database management, and web scraping with **Beautiful Soup** and **Playwright** for data retrieval.

---

## Features
- **Check Vacation Hot Offers**: View a list of hot vacation offers from different agencies. It displays the offer title, date, and price for each offer.
- **Check Budget**: Convert an amount from one currency to another. It supports conversion between MDL, USD, and EUR currencies.

---

## Prerequisites
**Python** and **Chromium** should be installed on your PC

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
source venv/bin/activate
```
For Windows:
```
python -m venv venv
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
5. Run the application:

For Mac/Linux:
```
python3 vacation_assistant.py 
```
For Windows:
```
python vacation_assistant.py 
```

---

# Usage

1. Select a travel agency from the dropdown menu, and click "Check Offers" to view the hot offers.
2. Enter the amount, select the currencies, and click "Check Budget" to convert the amount.

---
