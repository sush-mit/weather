import json

from weather_data import WeatherData
from  weather_provider import WeatherProvider

class WeatherBit(WeatherProvider):
    def get_api_url(self):
        location = f'{self.city}'

        if self.country:
            location = f'{location}, {self.country}'

        if self.state:
            location = f'{location}, {self.state}'

        url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={self.api_key}&include=minutely'

        return url

    def process(self, response):
        js = json.loads(response)
        temperature = js['data'][0]['temp']
        if self.unit == 'K':
            temperature += 272.15
        if isinstance(temperature, float):
            temperature = f'{temperature:.2f}'
        humidity = None
        weather = js['data'][0]['weather']['description']

        weather_data = WeatherData(temperature=temperature, humidity=humidity, weather=weather)
        return weather_data