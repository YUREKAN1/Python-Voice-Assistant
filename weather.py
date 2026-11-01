
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):

    if not API_KEY:
        return None, "Weather API key is missing."

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            return None, "City not found. Please try another city."

        response.raise_for_status()

        data = response.json()

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

        return weather_info, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to the weather service."

    except (KeyError, TypeError, ValueError):
        return None, "Received invalid weather data."
