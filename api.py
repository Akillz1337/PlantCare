import requests


def fetch_sensor_data():
    url = "https://plantcare-api-alb3.onrender.com/sensor"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None