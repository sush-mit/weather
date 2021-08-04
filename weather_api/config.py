import os
import sys
import configparser

import lists

class Config:

    config_filename = 'config.ini'

    def set_initial(self):
        config_parser = configparser.ConfigParser()
        if not os.path.isfile(Config.config_filename):
            for name in lists.PROVIDERS:
                config_parser.add_section(name)
            with open('config.ini', 'w') as configfile:
                config_parser.write(configfile)
        else:
            return

    def set_config(self, key, name):
        config_parser = configparser.ConfigParser()
        if not os.path.isfile(Config.config_filename):
            config_parser.add_section(name)
        else:
            config_parser.read(Config.config_filename)
            if not name in config_parser.sections():
                config_parser.add_section(name)
        config_parser.set(name, 'key', key)
        with open('config.ini', 'w') as configfile:
            config_parser.write(configfile)

    def get_config(self, name):
        config_parser = configparser.ConfigParser()
        if not os.path.isfile(Config.config_filename):
            sys.exit(f'{os.path.join(os.path.abspath("."),Config.config_filename)} file not found.')
        else:
            config_parser.read(Config.config_filename)
            if name in config_parser.sections():
                return config_parser[name]