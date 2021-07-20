import configparser
import sys
import argparse
from time import time
from config import Config
import datetime
import re

from weather_database_manager import DatabaseReader
from args_data import ArgsData
import lists

class ArgParse:
    def arg_parse(self):
        self.args_parse = argparse.ArgumentParser(description='Get weather of given location.')
        # General arguments
        self.args_parse.add_argument('--city', type=str, metavar='', help='City.')
        self.args_parse.add_argument('--state', type=str, metavar='', help='State.')
        self.args_parse.add_argument('--country', type=str, metavar='', help='Country.')
        self.args_parse.add_argument('--name', type=str, metavar='', choices=lists.PROVIDERS+[None], help='Provider name.')
        self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.')
        # Print arguements
        self.args_parse.add_argument('--unit', type=str, metavar='', choices=lists.UNITS, help='Units to print temperature in.', default='K')
        self.args_parse.add_argument('--interval', type=float, metavar='', help='Interval to check weather (seconds).')
        # Query arguments
        self.args_parse.add_argument('--date', type=datetime.date.fromisoformat, metavar='', help='Date in YYYY-MM-DD.')
        self.args_parse.add_argument('--get', type=str, metavar='', choices=lists.GETABLE_COLUMN_NAMES, help='Data to get (can be comma separated values).', default='all')
        self.args_parse.add_argument('--timeframe',type=self.timeframe, metavar='', help='Time frame to get weather data from ("Ny"/"Nm"/"Nd").', default='1d')
        self.args_parse.add_argument('--orderby', type=self.column_names, metavar='', help='Order data by.', default='id')
        self.args_parse.add_argument('--orderin', type=str, metavar='', choices=lists.ORDER_IN, help='Order data in.', default='ASC')
        self.args_parse.add_argument('--max', action='store_true', help='Get maximum value of following argument.')
        self.args_parse.add_argument('--min', action='store_true', help='Get minimum value of following argument.')
        self.args_parse.add_argument('--temperature', type=self.timeframe, metavar='', help='Get minimum value of following argument.', default='1d')
        self.args_parse.add_argument('--humidity', type=self.timeframe, metavar='', help='Get minimum value of following argument.', default='1d')

        mutually_exclusive = self.args_parse.add_mutually_exclusive_group()

        mutually_exclusive.add_argument('--config', action='store_true', help='config api.')
        mutually_exclusive.add_argument('--query', action='store_true', help='Get weather data from database.')
        self.args_parse.add_argument('-p', '--print', action='store_true', help='Print weather data to console.')
        mutually_exclusive.add_argument('-s', '--store', action='store_true', help='Store weather data in database.')

        args_proc = ArgsProc(self)
        self.args = self.args_parse.parse_args()

        return args_proc.process()

    def timeframe(self, input_):
        if not any(condition for condition in [re.match('[0-9]+d', input_), re.match('[0-9]+w', input_), re.match('[0-9]+m', input_), re.match('[0-9]+y', input_)]):
            raise argparse.ArgumentError
        else:
            return input_

    def column_names(self, input_):
        if input_ in lists.COLUMN_NAMES:
            return input_
        if input_ == 'temperature':
            return '"temperature (K)"'
        if input_ == 'humidity':
            return '"humidity (%)"'

class ArgsProc:
    def __init__(self, ap):
        self.config = Config()
        self.ap = ap
        self.filter_options = None
        self.search_terms = None

    def process(self):
        if self.ap.args.config:
            self.process_config()
        elif self.ap.args.query:
            self.process_query()
        else:
            if self.ap.args.city == None and self.ap.args.country == None and self.ap.args.state == None:
                sys.exit('Not enough arguments.')
            if self.ap.args.name == None:
                print('--name not specified, continuing with default: openweather')
                self.ap.args.name = 'openweather'
            config_parser = self.config.get_config(self.ap.args.name)
            self.ap.args.key = config_parser.get('key')
            if self.ap.args.key == None:
                sys.exit(f'Key is not set for {self.ap.args.name}')

        if self.ap.args.unit not in ['K', 'F', 'C']:
            print('Wrong arguement for --unit, continuing with default: K')
            self.ap.args.unit = 'K'

        return ArgsData(*vars(self.ap.args).values(), self.search_terms, self.filter_options)

    def process_config(self):
        if not any(arg for arg in [self.ap.args.name, self.ap.args.key]):
            error_msg = 'Missing required arguements for config: '
            if not self.ap.args.name:
                error_msg += '--name '
            if not self.ap.args.key:
                error_msg += '--key'
            sys.exit(error_msg)
        if self.ap.args.name not in lists.PROVIDERS:
            sys.exit(f'Invalid provider name: {self.ap.args.name}')
        name = self.ap.args.name
        self.config.set_config(self.ap.args.key, name)
        sys.exit(f'Settings saved to {Config.config_filename}.')

    def process_query(self):
        if not self.ap.args.city and not self.ap.args.date and not self.ap.args.max and not self.ap.args.min:
            sys.exit('Please set how to filter data.')
        if not self.ap.args.get:
            sys.exit(f'Please set which weather data to get: {lists.GETABLE_COLUMN_NAMES}')
        if self.ap.args.max or self.ap.args.min:
            if self.ap.args.temperature:
                self.ap.args.temperature = self.process_timeframe(self.ap.args.temperature)
                self.filter_options = '"temperature (K)"'
            elif self.ap.args.humidity:
                self.ap.args.humidity = self.process_timeframe(self.ap.args.humidity)
                self.filter_options = '"humidity (%)"'
        elif self.ap.args.timeframe:
            self.ap.args.timeframe = self.process_timeframe(self.ap.args.timeframe)
            self.filter_options = [filter_option for filter_option in ['city', 'date'] if self.ap.args.__getattribute__(filter_option)]
        self.search_terms = [search_term for search_term in [self.ap.args.city, self.ap.args.date] if search_term]

    def process_timeframe(self, timeframe):
            if re.match('[0-9]+d', timeframe):
                timeframe = f'-{timeframe[:-1]} day'
            elif re.match('[0-9]+w', timeframe):
               timeframe = f'-{timeframe[:-1]} week'
            elif re.match('[0-9]+m', timeframe):
                timeframe = f'-{timeframe[:-1]} month'
            elif re.match('[0-9]+y', timeframe):
                timeframe = f'-{timeframe[:-1]} year'
            return timeframe
