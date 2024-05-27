import pytest
from unittest.mock import patch, Mock, ANY
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from weather_fetcher import fetch_weather_forecast, extract_daily_forecasts, fetch_weather_icon

# Mock data for testing
mock_current_weather_data = {
    "coord": {"lat": 51.5085, "lon": -0.1257},
    "weather": [{"description": "clear sky", "icon": "01d"}],
    "main": {"temp": 300.15},
    "name": "London",
    "dt": 1716835678  # Timestamp for Monday, May 27, 2024
}

mock_forecast_data = {
    "list": [
        {"dt_txt": "2021-01-01 12:00:00", "main": {"temp": 289.15}, "weather": [{"description": "cloudy"}]},
        {"dt_txt": "2021-01-02 12:00:00", "main": {"temp": 292.15}, "weather": [{"description": "sunny"}]},
    ]
}


@patch('weather_fetcher.requests.get')
def test_fetch_weather_forecast(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_current_weather_data),
        Mock(status_code=200, json=lambda: mock_forecast_data)
    ]
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    
    weather_data, daily_forecasts = fetch_weather_forecast("London", "fake_api_key", current_weather_url, forecast_url)
    
    assert weather_data['city'] == "London"
    assert weather_data['temperature'] == 27  # 300.15 - 273.15
    assert weather_data['description'] == "clear sky"
    assert weather_data['icon'] == "01d"
    assert weather_data['day'] == "Monday"
    
    assert len(daily_forecasts) == 2
    assert daily_forecasts[0]['dt_txt'] == "2021-01-01 12:00:00"
    assert daily_forecasts[1]['dt_txt'] == "2021-01-02 12:00:00"


def test_extract_daily_forecasts():
    daily_forecasts = extract_daily_forecasts(mock_forecast_data)
    assert len(daily_forecasts) == 2
    assert daily_forecasts[0]['dt_txt'] == "2021-01-01 12:00:00"
    assert daily_forecasts[1]['dt_txt'] == "2021-01-02 12:00:00"


@patch('weather_fetcher.requests.get')
@patch('weather_fetcher.Image.open')
@patch('weather_fetcher.ImageTk.PhotoImage')
def test_fetch_weather_icon(mock_photoimage, mock_open, mock_get):
    # Mock the requests.get response
    mock_get.return_value = Mock(status_code=200, content=b'binary image data')

    # Mock the Image.open response
    mock_image = Mock()
    mock_open.return_value = mock_image

    # Mock the ImageTk.PhotoImage response
    mock_photo = Mock()
    mock_photoimage.return_value = mock_photo

    icon_code = "01d"
    photo = fetch_weather_icon(icon_code)

    assert photo is mock_photo
    mock_get.assert_called_once_with(f"http://openweathermap.org/img/w/{icon_code}.png")
    mock_open.assert_called_once_with(ANY)
    mock_photoimage.assert_called_once_with(mock_image)

if __name__ == '__main__':
    pytest.main()
