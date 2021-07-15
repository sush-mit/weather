import json

from weather_data import WeatherData
from weather_provider import WeatherProvider

class WeatherAPI(WeatherProvider):
    def get_api_url(self):
        location = f'{self.city}'

        if self.country:
            location = f'{location}, {self.country}'

        if self.state:
            location = f'{location}, {self.state}'

        url = f'http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={location}&aqi=no'

        return url

    def process(self, js):
        js = json.loads(js)
        temperature = int(js['current']['temp_c'])
        temperature += 272.15 # Converting celsius to kelvin
        humidity = js['current']['humidity']
        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'
        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'
        weather = js['current']['condition']['text']

        weather_data = WeatherData(temperature=temperature, humidity=humidity, weather=weather)

        return weather_data