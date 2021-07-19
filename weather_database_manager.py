import sqlite3
import sys
import datetime

from weather_database import DatabaseWriter, DatabaseReader
import printer

class WeatherDatabaseManager:

    def update_database(weather_obj, city):
            temperature = weather_obj.temperature
            humidity = weather_obj.humidity
            weather = weather_obj.weather
            date = weather_obj.date
            time = f'{weather_obj.time.hour}:{weather_obj.time.minute}:{weather_obj.time.second}'

            database_writer = DatabaseWriter()
            database_writer.set_database()
            database_writer.create_database()
            database_writer.update_database(city, temperature, humidity, weather, date, time)

    def get_database(order_by=None, order_in='ASC', filter_option=None, search_terms=None):
        database_reader = DatabaseReader()
        database_reader.set_database()
        database_data = database_reader.sqlite_select(order_by=order_by, order_in='ASC', filter_option=filter_option, search_terms=search_terms)
        printer.database_weather_data(database_data)