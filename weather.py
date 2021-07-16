import sys
import time
import json

from config import Config
from arg_parse import ArgParse
from weather_factory import WeatherProviderFactory

class Weather:
    def get_weather(self, api_key, city, unit, name="openweather", country = None, state = None):
        weather_provider = WeatherProviderFactory().get(name)
        weather_provider.api_key = api_key
        weather_provider.city = city
        weather_provider.country = country
        weather_provider.state = state
        weather_provider.unit = unit

        weather_data = weather_provider.fetch()
        return weather_data

if __name__=='__main__':
    Config().set_initial()
    ap = ArgParse()
    w = Weather()

    weather = w.get_weather(city=ap.args.city, state=ap.args.state, country=ap.args.country, api_key=ap.key, name=ap.args.name, unit=ap.args.unit)

    if ap.args.unit.upper() == 'F':
        weather.to_farenheit()
    if ap.args.unit.upper() == 'C':
        weather.to_celsius()

    while True:
        print(f'\nTemperature: {weather.temperature}{ap.args.unit.upper()}\nHumidity: {weather.humidity}%\nWeather condition: {weather.weather}')
        if not ap.args.interval:
            sys.exit()
        time.sleep(ap.args.interval)