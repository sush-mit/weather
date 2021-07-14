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

        temerature = int(response['main']['temp'])
        temerature -= 272.15

        if isinstance(temerature, float):
            temerature = f'{temerature:.2f}'

        humidity = response['main']['humidity']

        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'

        weather = response['weather'][0]['main']

        data = WeatherData(temperature=temerature, humidity=humidity, weather=weather)

        return data