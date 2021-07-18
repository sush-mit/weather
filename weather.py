import sys
import time
import json

from config import Config
from arg_parse import ArgParse
from weather_factory import WeatherProviderFactory
from weather_database_manager import WeatherDatabaseManager

class Weather:
    def get_weather(api_key, city, unit, name="openweather", country = None, state = None):
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
    w = Weather

    if ap.args.query:
        WeatherDatabaseManager.get_database(order_by=ap.args.orderby, order_in=ap.args.orderin, filter_option=ap.filter_options, search_terms=ap.search_terms)
        sys.exit()
    weather = w.get_weather(city=ap.args.city, state=ap.args.state, country=ap.args.country, api_key=ap.key, name=ap.args.name, unit=ap.args.unit)
    if ap.args.store:
        WeatherDatabaseManager.update_database(weather_obj=weather, city=ap.args.city)

    while True:
        print(f'\nTemperature: {weather.temperature}{ap.args.unit.upper()}\nHumidity: {weather.humidity}%\nWeather condition: {weather.weather}')
        if not ap.args.interval:
            sys.exit()
        time.sleep(ap.args.interval)