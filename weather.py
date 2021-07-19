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
        if ap.args.max or ap.args.min:
            if ap.args.max:
                if ap.args.temperature:
                    database_data = WeatherDatabaseManager.get_max(timeframe=ap.args.temperature, filter_option=ap.filter_options, city=ap.args.city)
                elif ap.args.humidity:
                    database_data = WeatherDatabaseManager.get_max(timeframe=ap.args.humidity, filter_option=ap.filter_options, city=ap.args.city)
            if ap.args.min:
                if ap.args.temperature:
                    database_data = WeatherDatabaseManager.get_min(timeframe=ap.args.temperature, filter_option=ap.filter_options, city=ap.args.city)
                elif ap.args.humidity:
                    database_data = WeatherDatabaseManager.get_min(timeframe=ap.args.humidity, filter_option=ap.filter_options, city=ap.args.city)
        else:
            database_data = WeatherDatabaseManager.get_database(order_by=ap.args.orderby, order_in=ap.args.orderin, filter_option=ap.filter_options, search_terms=ap.search_terms, timeframe=ap.args.timeframe)
        filter_get.filter_get(database_data, ap)
    else:
        weather = w.get_weather(city=ap.args.city, state=ap.args.state, country=ap.args.country, api_key=ap.key, name=ap.args.name, unit=ap.args.unit)
        while True:
            if ap.args.print:
                printer.weather_data(weather, ap)
            if ap.args.store:
                WeatherDatabaseManager.update_database(weather_obj=weather, city=ap.args.city)
            if not ap.args.interval:
                sys.exit()
            time.sleep(ap.args.interval)
