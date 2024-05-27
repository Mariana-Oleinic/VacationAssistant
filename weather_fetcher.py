from datetime import datetime
from io import BytesIO
import requests
from PIL import Image, ImageTk


def fetch_weather_forecast(city, api_key, current_weather_url, forecast_url):
    """
    Fetches the current weather and daily forecasts for a given city.
    Args:
    - city (str): The name of the city.
    - api_key (str): The API key for accessing the weather API.
    - current_weather_url (str): The URL template for fetching current weather data.
    - forecast_url (str): The URL template for fetching forecast data.
    Returns:
    - Tuple[dict, list]: A tuple containing the current weather data and daily forecasts.
                         Returns (None, None) if the request fails.
    """
    current_weather_response = requests.get(current_weather_url.format(city, api_key))
    if current_weather_response.status_code == 200:
        data = current_weather_response.json()
        lat, lon = data['coord']['lat'], data['coord']['lon']
        weather_data = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"] - 273.15),
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            'day': datetime.fromtimestamp(data['dt']).strftime('%A')
        }
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key))
        if forecast_response.status_code == 200:
            data2 = forecast_response.json()
            daily_forecasts = extract_daily_forecasts(data2)
            return weather_data, daily_forecasts
    else:
        return None, None
  

def extract_daily_forecasts(response):
    """
    Extracts daily forecasts from the API response.
    Args:
   - response (dict): The API response containing forecast data for multiple days and at different hours.
    Returns:
    - list: A list of daily forecasts at specified time 12:00:00.
    """
    daily_forecasts = {}
    for forecast in response['list']:
        date, time = forecast['dt_txt'].split(" ")
        if date != datetime.now() not in daily_forecasts or time == "12:00:00":
            daily_forecasts[date] = forecast

    return list(daily_forecasts.values())


def fetch_weather_icon(icon_code):
    """
    Fetches the weather icon from OpenWeatherMap using the provided icon code.
    Args:
    - icon_code (str): The code of the weather icon.
    Returns:
    - ImageTk.PhotoImage: The weather icon as a PhotoImage object for use in Tkinter.
    """
    icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
    response = requests.get(icon_url)
    
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)
        return photo
    else:
        raise ValueError(f"Failed to fetch weather icon. Status code: {response.status_code}")
    