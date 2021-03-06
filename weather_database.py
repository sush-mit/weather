import sqlite3
import sys
import datetime

from database_weather_data import DatabaseWeatherData

class WeatherDatabase:
    database_file = '.\\weather.db'
    table_name = 'weatherDatabase'

    def set_database(self):
        self.conn = sqlite3.connect(WeatherDatabase.database_file)
        self.c = self.conn.cursor()

class DatabaseWriter(WeatherDatabase):
    def create_database(self):
        self.c.execute(f""" CREATE TABLE IF NOT EXISTS {WeatherDatabase.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            state TEXT,
            country TEXT,
            "temperature (K)" REAL,
            "humidity (%)" REAL,
            weather TEXT,
            date DATE,
            time TEXT
        )""")
        self.conn.commit()

    def update_database(self, city, state, country, temperature, humidity, weather, date, time):
        try:
            self.c.execute(f"""INSERT INTO {DatabaseReader.table_name} (city, state, country, "temperature (K)", "humidity (%)", weather, date, time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (city, state, country, temperature, humidity, weather, date, time))
        except BaseException as e:
            if 'UNIQUE constraint failed' in ' '.join(e.args):
                pass
            else:
                print(e)
        self.conn.commit()

        
class DatabaseReader(WeatherDatabase):
    def sqlite_select(self, timeframe, order_by=None, order_in='ASC', filter_option=None, search_terms=None):
        command = self.get_command(order_by=order_by, order_in=order_in, filter_option=filter_option, search_terms=search_terms, timeframe=timeframe)
        return self.execute(command=command)

    def get_command(self, order_by, order_in, filter_option, search_terms, timeframe):
        command = f"""SELECT * FROM {WeatherDatabase.table_name}"""
        if filter_option != None and search_terms != None:
            command += ' WHERE'
            for item in zip(filter_option, search_terms):
                command += f""" {item[0]} = '{item[1]}'"""
                if filter_option.index(item[0]) != len(filter_option)-1:
                    command += ' AND'
            command += f' AND date > date(date, "{timeframe}")'
        if order_by != None and order_in != None:
            command +=  f' ORDER BY {order_by} {order_in}'
        return command

    def sqlite_select_max(self, timeframe, filter_option=None, city=None):
        command = self.get_command_max(timeframe, filter_option, city)
        return self.execute(command=command)

    def get_command_max(self, timeframe, filter_option=None, city=None):
        command = f"""SELECT * FROM {self.table_name} WHERE {filter_option} = (SELECT MAX({filter_option}) FROM {self.table_name} WHERE date > date(date, "{timeframe}")"""
        if city != None:
            command += f' AND city = "{city}"'
        command += f""")"""
        return command

    def sqlite_select_min(self, timeframe, filter_option=None, search_terms=None, city=None):
        command = self.get_command_min(timeframe, filter_option, city)
        return self.execute(command=command)
    
    def get_command_min(self, timeframe, filter_option=None, city=None):
        command = f"""SELECT * FROM {self.table_name} WHERE {filter_option} = (SELECT MIN({filter_option}) FROM {self.table_name} WHERE date > date(date, "{timeframe}")"""
        if city != None:
            command += f' AND city = "{city}"'
        command += f""")"""
        return command

    def execute(self, command):
        try:
            self.c.execute(command)
        except sqlite3.OperationalError as e:
            if 'no such table' in e.args[0]:
                pass
            else:
                error_msg = f"Error reading FROM {WeatherDatabase.table_name}:\n{' '.join(e.args)}"
                sys.exit(error_msg)
        results = [result for result in self.c.fetchall()]
        return self.parse(results)

    def parse(self, results):
        for result in results:
            id_ = result[0]
            city = result[1]
            state = result[2]
            country = result[3]
            temperature = result[4]
            humidity = result[5]
            weather = result[6]
            date = (datetime.datetime.strptime(results[0][7], '%Y-%m-%d')).date()
            time = (datetime.datetime.strptime(results[0][8], '%H:%M:%S')).time()
            yield DatabaseWeatherData(id_, city, state, country, temperature, humidity, weather, date, time)