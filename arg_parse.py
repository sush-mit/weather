import sys
import argparse
from time import time
from config import Config
import datetime
import re

from weather_database_manager import DatabaseReader
import lists

class ArgParse:
    def __init__(self):
        self.config = Config()
        self.args_parse = argparse.ArgumentParser(description='Get weather of given location.')
        self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.', default='a85e593a075e92f3b7285c21b42811ae')
        self.args_parse.add_argument('--city', type=str, metavar='', help='City.')
        self.args_parse.add_argument('--state', type=str, metavar='', help='State.')
        self.args_parse.add_argument('--country', type=str, metavar='', help='Country.')
        self.args_parse.add_argument('--unit', type=str, metavar='', choices=lists.units, help='Units to print temperature in.', default='K')
        self.args_parse.add_argument('--interval', type=float, metavar='', help='Interval to check weather (seconds).')
        self.args_parse.add_argument('--name', type=str, metavar='', choices=lists.providers, help='Provider name.', default='openweather')
        self.args_parse.add_argument('-p', '--print', action='store_true', help='Print weather data to console.')

        mutually_exclusive = self.args_parse.add_mutually_exclusive_group()

        mutually_exclusive.add_argument('--config', action='store_true', help='config api.')
        self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.')
        mutually_exclusive.add_argument('--query', action='store_true', help='Get weather data from database.')
        self.args_parse.add_argument('--date', type=datetime.date.fromisoformat, metavar='', help='Date in YYYY-MM-DD.')
        self.args_parse.add_argument('--get', type=str, metavar='', choices=lists.getable_column_names, help='Data to get (can be comma separated values).')
        self.args_parse.add_argument('--timeframe',type=self.timeframe, metavar='', help='Time frame to get weather data from ("Ny"/"Nm"/"Nd").', default='1d')
        self.args_parse.add_argument('--orderby', type=str, metavar='', choices=lists.getable_column_names, help='Order data by.')
        self.args_parse.add_argument('--orderin', type=str, metavar='', choices=lists.order_in, help='Order data in.', default='ASC')
        mutually_exclusive.add_argument('-s', '--store', action='store_true', help='Store weather data in database.')
        args_proc = ArgsProc(self)
        self.args = self.args_parse.parse_args()
        args_proc.process()

    def timeframe(self, input_):
        if not any(condition for condition in [re.match('[0-9]+d', input_), re.match('[0-9]+w', input_), re.match('[0-9]+m', input_), re.match('[0-9]+y', input_)]):
            raise argparse.ArgumentError
        else:
            return input_

class ArgsProc:
    def __init__(self, ap):
        self.ap = ap
    def process(self):
        if self.ap.args.config:
            self.process_config()
        elif self.ap.args.query:
            self.process_query()
        else:
            if self.ap.args.city == None and self.ap.args.country == None and self.ap.args.state == None:
                sys.exit('Not enough arguments.')
<<<<<<< HEAD
            if self.args.name not in Config.API_NAMES:
                sys.exit(f'Invalid provider name: {self.args.name}')
            if self.args.name == None:
=======
            if self.ap.args.name == None:
>>>>>>> optimized arg_parse.py
                print('--name not specified, continuing with default: openweather')
                self.ap.args.name = 'openweather'
            config_parser = self.ap.config.get_config(self.ap.args.name)
            self.ap.key = config_parser.get('key')
            if self.ap.key == None:
                sys.exit(f'Key is not set for {self.ap.args.name}')

<<<<<<< HEAD
        if self.args.unit not in ['K', 'F', 'C']:
            print('Wrong arguement for --unit, continuing with default: K')
            self.args.unit = 'K'
=======
        if not self.ap.args.unit:
            self.ap.args.unit = 'C'
            print('--unit not specified, continuing with default: C')
        if self.ap.args.unit not in ['C', 'K']:
            print('Wrong arguement for --unit, continuing with default: C.')
            self.ap.args.unit = 'C'

    def process_config(self):
        if not any(arg for arg in [self.ap.args.name, self.ap.args.key]):
            error_msg = 'Missing required arguements for config: '
            if not self.ap.args.name:
                error_msg += '--name '
            if not self.ap.args.key:
                error_msg += '--key'
            sys.exit(error_msg)
        if self.ap.args.name not in Config.API_NAMES:
            sys.exit(f'Invalid provider name: {self.ap.args.name}')
        self.ap.key = self.ap.args.key
        name = self.ap.args.name
        self.ap.config.set_config(self.ap.key, name)
        sys.exit(f'Settings saved to {Config.config_filename}.')

    def process_query(self):
        if not self.ap.args.city and not self.ap.args.date:
            sys.exit('Please set city name or date to get weather data from.')
        if not self.ap.args.get:
            sys.exit(f'Please set which weather data to get: {DatabaseReader.getable_column_names}')
        self.ap.filter_options = [filter_option for filter_option in ['city', 'date'] if self.ap.args.__getattribute__(filter_option)]
        gets = [get for get in self.ap.args.get.split(',')]
        if self.ap.args.timeframe:
            if re.match('[0-9]+d', self.ap.args.timeframe):
                self.ap.args.timeframe = f'-{self.ap.args.timeframe[:-1]} day'
            elif re.match('[0-9]+w', self.ap.args.timeframe):
                self.ap.args.timeframe = f'-{self.ap.args.timeframe[:-1]} week'
            elif re.match('[0-9]+m', self.ap.args.timeframe):
                self.ap.args.timeframe = f'-{self.ap.args.timeframe[:-1]} month'
            elif re.match('[0-9]+y', self.ap.args.timeframe):
                self.ap.args.timeframe = f'-{self.ap.args.timeframe[:-1]} year'
        self.ap.search_terms = [search_term for search_term in [self.ap.args.city, self.ap.args.date] if search_term]
>>>>>>> optimized arg_parse.py
