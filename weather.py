import sys
import time
import json
import argparse
import configparser
import os
import re

import mechanize

API_NAMES = ['open-weather', 'weather-api']

class WeatherData:
    def __init__(self, temperature, humidity, weather):
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather

class WeatherAPI:
    def get_api_url(self, location, key):
        self.location = location
        self.key = key
        url = f'http://api.weatherapi.com/v1/current.json?key={self.key}&q={self.location}&aqi=no'
        return url
    def fetch(self, url):
        try:
            res = mechanize.urlopen(url)
        except mechanize.HTTPError as e:
            if e.getcode() == 404:
                sys.exit(f'city/state/country "{self.location}" not found.')
            else:
                sys.exit(e)
        read = res.read()
        js = json.loads(read)
        return self.process(js)

    def process(self, js):
        temerature = int(js['current']['temp_c'])
        humidity = js['current']['humidity']
        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'
        weather = js['current']['condition']['text']

        weather_data = WeatherData(temperature=temerature, humidity=humidity, weather=weather)

        return weather_data

class OpenWeather:
    def get_api_url(self, location, key):
        self.location = location
        self.key = key
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}'
        return url

    def fetch(self, url):
        try:
            res = mechanize.urlopen(url)
        except mechanize.HTTPError as e:
            if e.getcode() == 404:
                sys.exit(f'city/state/country "{self.location}" not found.')
            else:
                sys.exit(e)
        read = res.read()
        js = json.loads(read)
        return self.process(js)

    def process(self, js):
        temerature = int(js['main']['temp'])
        temerature -= 272.15
        if isinstance(temerature, float):
            temerature = f'{temerature:.2f}'
        humidity = js['main']['humidity']
        if isinstance(humidity, float):
            humidity = f'{humidity:.2f}'
        weather = js['weather'][0]['main']

        weather_data = WeatherData(temperature=temerature, humidity=humidity, weather=weather)

        return weather_data

class WeatherProviderFactory:
    def get(self, provider):
        if provider == 'open-weather':
            return OpenWeather()
        elif provider == 'weather-api':
            return WeatherAPI()

class Config:

    config_filename = 'config.ini'

    def set_initial(self):
        config_parser = configparser.ConfigParser()
        if not os.path.isfile(Config.config_filename):
            for name in API_NAMES:
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

class Weather:
    def get_weather(self, city, country, state, key, name):
        # key = 'a85e593a075e92f3b7285c21b42811ae'
        location = ''

        if city != None:
            location += city
            if state != None:
                location += f',{state}'
            if country != None:
                location += f',{country}'

        weather_provider = WeatherProviderFactory().get(name)
        url = weather_provider.get_api_url(location=location, key=key)
        weather_data = weather_provider.fetch(url=url)
        return weather_data

class Argparse:
    def __init__(self):
        self.config = Config()
        self.args_parse = argparse.ArgumentParser(description='Get weather of given location.')
        self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.')
        self.args_parse.add_argument('--city', type=str, metavar='', help='City.')
        self.args_parse.add_argument('--state', type=str, metavar='', help='State.')
        self.args_parse.add_argument('--country', type=str, metavar='', help='Country.')
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
            if self.args.name not in API_NAMES:
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

if __name__=='__main__':
    Config().set_initial()
    ap = Argparse()
    w = Weather()
    weather = w.get_weather(city=ap.args.city, state=ap.args.state, country=ap.args.country, key=ap.key, name=ap.args.name)
    while True:
        print(f'Temperature: {weather.temperature}C\nHumidity: {weather.humidity}%\nWeather condition: {weather.weather}')
        if not ap.args.interval:
            sys.exit()
        time.sleep(ap.args.interval)