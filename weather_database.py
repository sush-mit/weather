import sqlite3
import sys

from database_weather_data import DatabaseWeatherData

class WeatherDatabase:
    database_file = '.\\weather.db'
    table_name = 'weatherDatabase'
    getable_column_names = ['temperature', 'humidity', 'weather']

    def set_database(self):
        print('setting')
        self.conn = sqlite3.connect(WeatherDatabase.database_file)
        self.c = self.conn.cursor()
        print('set')

class DatabaseWriter(WeatherDatabase):
    def create_database(self):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS weatherDatabase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            "temperature (K)" REAL,
            "humidity (%)" REAL,
            weather TEXT,
            date DATE,
            time TEXT
        )""")
        self.conn.commit()

class DatabaseReader(WeatherDatabase):
    def sqlite_select(self, order_by=None, order_in='ASC', filter_option=None, search_terms=None):
        command = self.get_command(order_by=order_by, order_in=order_in, filter_option=filter_option, search_terms=search_terms)
        return self.execute(command=command)

    def get_command(self, order_by, order_in, filter_option, search_terms):
        command = f"""SELECT * FROM {WeatherDatabase.table_name}"""
        if filter_option != None and search_terms != None:
            command += ' WHERE'
            for item in zip(filter_option, search_terms):
                command += f""" {item[0]} = '{item[1]}'"""
                if filter_option.index(item[0]) != len(filter_option)-1:
                    command += ' AND'
        if order_by != None and order_in != None:
            command +=  f' ORDER BY {order_by} {order_in}'
        return command

    def execute(self, command):
        try:
            self.cur.execute(command)
        except sqlite3.OperationalError as e:
            if 'no such table' in e.args[0]:
                pass
            else:
                error_msg = f"Error reading FROM {WeatherDatabase.table_name}:\n{' '.join(e.args)}"
                sys.exit(error_msg)
        results = [result for result in self.cur.fetchall()]
        return self.parse(results)

    def parse(self, results):
        pass

# if __name__ == '__main__':
#     dbw = DatabaseWriter()
#     dbw.set_database()
#     dbw.create_database()