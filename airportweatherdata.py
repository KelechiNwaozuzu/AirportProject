import requests
import pandas as pd

locationUrl = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Atlanta?unitGroup=metric&key=2TVBWPA2NTYXSF2A9GJQEJDAA&contentType=json"


params = {
    "unitGroup": "imperial", 
    "key": "2TVBWPA2NTYXSF2A9GJQEJDAA",
    "contentType": "json"
}

r = requests.get(locationUrl, params=params)
data = r.json()


timeStamps = data['days']
weatherData = []

for day in timeStamps:
    weatherPoint = {
        'time': day['datetime'],
        'temperature': day['tempmax'],
        'weatherCode': day['conditions'],
        'precipitationProb': day['precipprob']
    }
    weatherData.append(weatherPoint)

df = pd.DataFrame(weatherData)

df.to_csv('AtlantaWeather.csv', index = False)

print("Weather data has been saved to your Atlanta Weather CSV")
