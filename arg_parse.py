import sys
import argparse
from config import Config
import datetime

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
        self.args_parse.add_argument('--timeframe', type=str, metavar='', help='Time frame to get weather data from ("Ny"/"Nm"/"Nd").', default='1d')
        self.args_parse.add_argument('--orderby', type=str, metavar='', choices=lists.getable_column_names, help='Order data by.')
        self.args_parse.add_argument('--orderin', type=str, metavar='', choices=lists.order_in, help='Order data in.', default='ASC')
        mutually_exclusive.add_argument('-s', '--store', action='store_true', help='Store weather data in database.')
        self.process()

    def process(self):
        self.args = self.args_parse.parse_args()
        if self.args.config:
            if not any(arg for arg in [self.args.name, self.args.key]):
                error_msg = 'Missing required arguements for config: '
                if not self.args.name:
                    error_msg += '--name '
                if not self.args.key:
                    error_msg += '--key'
                sys.exit(error_msg)
            if self.args.name not in Config.API_NAMES:
                sys.exit(f'Invalid provider name: {self.args.name}')
            self.key = self.args.key
            name = self.args.name
            self.config.set_config(self.key, name)
            sys.exit(f'Settings saved to {Config.config_filename}.')

        elif self.args.query:
            if not self.args.city and not self.args.date:
                sys.exit('Please set city name or date to get weather data from.')
            if not self.args.get:
                sys.exit(f'Please set which weather data to get: {DatabaseReader.getable_column_names}')
            self.filter_options = [filter_option for filter_option in ['city', 'date'] if self.args.__getattribute__(filter_option)]
            gets = [get for get in self.args.get.split(',')]
            self.search_terms = [search_term for search_term in [self.args.city, self.args.date] if search_term]

        else:
            if self.args.city == None and self.args.country == None and self.args.state == None:
                sys.exit('Not enough arguments.')
            if self.args.name not in Config.API_NAMES:
                sys.exit(f'Invalid provider name: {self.args.name}')
            if self.args.name == None:
                print('--name not specified, continuing with default: openweather')
                self.args.name = 'openweather'
            config_parser = self.config.get_config(self.args.name)
            self.key = config_parser.get('key')
            if self.key == None:
                sys.exit(f'Key is not set for {self.args.name}')

        if self.args.unit not in ['K', 'F', 'C']:
            print('Wrong arguement for --unit, continuing with default: K')
            self.args.unit = 'K'
