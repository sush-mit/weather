import sys
import time
import json

from config import Config
from arg_parse import ArgParse
from weather_factory import WeatherProviderFactory
from weather_database_manager import WeatherDatabaseManager
import printer
import filter_get

class Weather:
    def get_weather(api_key, city, unit, name, country = None, state = None):
        weather_provider = WeatherProviderFactory().get(name)
        weather_provider.api_key = api_key
        weather_provider.city = city
        weather_provider.country = country
        weather_provider.state = state
        weather_provider.unit = unit

        weather_data = weather_provider.fetch()

        if ap.unit.upper() == 'F':
            weather_data.to_farenheit()
        if ap.unit.upper() == 'C':
            weather_data.to_celsius()

        return weather_data

if __name__=='__main__':
    Config().set_initial()
    ap = ArgParse().arg_parse()
    w = Weather

    if ap.query:
        if ap.max or ap.min:
            if ap.max:
                if ap.temperature:
                    database_data = WeatherDatabaseManager.get_max(timeframe=ap.temperature, filter_option=ap.filter_options, city=ap.city)
                elif ap.humidity:
                    database_data = WeatherDatabaseManager.get_max(timeframe=ap.humidity, filter_option=ap.filter_options, city=ap.city)
            if ap.min:
                if ap.temperature:
                    database_data = WeatherDatabaseManager.get_min(timeframe=ap.temperature, filter_option=ap.filter_options, city=ap.city)
                elif ap.humidity:
                    database_data = WeatherDatabaseManager.get_min(timeframe=ap.humidity, filter_option=ap.filter_options, city=ap.city)
        else:
            database_data = WeatherDatabaseManager.get_database(order_by=ap.orderby, order_in=ap.orderin, filter_option=ap.filter_options, search_terms=ap.search_terms, timeframe=ap.timeframe)
        filter_get.filter_get(database_data, ap)
    else:
        weather = w.get_weather(city=ap.city, state=ap.state, country=ap.country, api_key=ap.key, name=ap.name, unit=ap.unit)

        while True:
            if ap.store:
                WeatherDatabaseManager.update_database(weather_obj=weather, city=ap.city, state=ap.state, country=ap.country)
            if ap.print:
                printer.weather_data(weather, ap)
            if not ap.interval:
                sys.exit()
            time.sleep(ap.interval)
