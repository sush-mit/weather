import sqlite3
import sys
import datetime

from weather_database import DatabaseWriter, DatabaseReader

class WeatherDatabaseManager:
    def update_database(weather_obj, city):
        temperature: float
        humidity: float
        weather: str
        date: datetime.date
        time: str

        def parse():
            temperature = weather_obj.temperature
            humidity = weather_obj.humidity
            weather = weather_obj.weather
            date = weather_obj.date
            time = weather_obj.time

        database_writer = DatabaseWriter()
        database_writer.set_database()
        database_writer.create_database()
        try:
            database_writer.c.execute(f"""INSERT INTO {DatabaseReader.table_name} (id, city, temperature, humidity, weather, date, time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (city, temperature, humidity, weather, date, time))
        except BaseException as e:
            if 'UNIQUE constraint failed' in ' '.join(e.args):
                pass
        database_writer.conn.commit()

    def get_database(order_by=None, order_in='ASC', filter_option=None, search_terms=None):
        database_reader = DatabaseReader()
        database_data = database_reader.sqlite_select(order_by=None, order_in='ASC', filter_option=filter_option, search_terms=search_terms)
        return database_data