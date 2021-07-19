import datetime

from weather_provider import WeatherProvider
from weather_data import WeatherData
import json

class OpenWeather(WeatherProvider):
    def get_api_url(self):
        location = f'{self.city}'

        if self.country:
            location = f'{location}, {self.country}'

        if self.state:
            location = f'{location}, {self.state}'

        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}'

        return url

    def process(self, response):
        response = json.loads(response)

        temperature = int(response['main']['temp'])
        humidity = response['main']['humidity']
        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'
        weather = response['weather'][0]['main']

        data = WeatherData(temperature=temperature, humidity=humidity, weather=weather)

        return data