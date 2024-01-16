from django.test import TestCase
import requests
# Create your tests here.
latitude = '52.52'
longitude = '13.419998'
num_days = 5
url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&past_days={num_days}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'

# https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&past_days={num_days}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m

response = requests.get(url)

if response.status_code == 200:
        print('TRue--------------Stataus')
        data = response.content
        print(response,'TRue--------------Stataus')
        print(data)
else:
    print('Failed to fetch weather data from Open Meteo.')