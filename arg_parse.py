import sys
import argparse
from config import Config

class ArgParse:
    def __init__(self):
        self.config = Config()
        self.args_parse = argparse.ArgumentParser(description='Get weather of given location.')
        self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.')
        self.args_parse.add_argument('--city', type=str, metavar='', help='City.')
        self.args_parse.add_argument('--state', type=str, metavar='', help='State.')
        self.args_parse.add_argument('--country', type=str, metavar='', help='Country.')
        self.args_parse.add_argument('--unit', type=str, metavar='', help='Units to print temperature in ("K" or "C").')
        self.args_parse.add_argument('--interval', type=float, metavar='', help='Interval to check weather (seconds).')
        self.args_parse.add_argument('--name', type=str, metavar='', help='Provider name.')
        mutually_exclusive = self.args_parse.add_mutually_exclusive_group()
        mutually_exclusive.add_argument('--config', action='store_true', help='config api.')
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
        else:
            if self.args.city == None and self.args.country == None and self.args.state == None:
                sys.exit('Not enough arguments.')
            name = self.args.name
            config_parser = self.config.get_config(name)
            self.key = config_parser.get('key')

        if self.args.unit not in ['C', 'K']:
            print('Wrong arguement for --unit, continuing with default "C".')
            self.args.unit = 'C'
        if not self.args.unit:
            self.args.unit = 'C'
