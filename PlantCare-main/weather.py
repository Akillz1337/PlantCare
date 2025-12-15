import requests


def fetch_weather(latitude=60.98, longitude=25.66):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m&timezone=auto"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['current']['temperature_2m'],
            'humidity': data['current']['relative_humidity_2m']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None