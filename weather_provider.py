import sys

import requests
from urllib3 import exceptions

class WeatherProvider:
    def __init__(self):
        self.country = None
        self.state = None

    def get_api_url(self):
        pass

    def fetch(self):
        try:
            response = requests.get(self.get_api_url())
            if response.status_code == 404:
                sys.exit(print(f'no city called "{self.city}" found.'))
        except requests.exceptions.ConnectionError as e:
            sys.exit(print(f'Device is not connected to the internet. Please check connection and try again.'))
        return self.process(response.content)

    def process(self, response):
        pass

