import requests
import pandas as pd


def fetchWeatherData(outputFile='atlweather.csv'):

    url = "https://api.tomorrow.io/v4/weather/realtime"

    params = {
        "location": "33.753746,-84.386330",  
        "units": "imperial",
        "apikey": "E0oe3K6YxiPv7sHqllVS5ir0bEnHWt8j"
    }

    response = requests.get(url, params=params)
    data = response.json()

    weather_data = {
        'temperature': data['data']['values']['temperature'],
        'weathercode': data['data']['values']['weatherCode'],
        'precProb': data['data']['values']['precipitationProbability']
    }

    df = pd.DataFrame([weather_data])

    df.to_csv(outputFile, index=False)

    print(f"Weather data saved to {outputFile}")


fetchWeatherData()
