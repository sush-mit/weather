from abc import ABC, abstractmethod
from typing import DefaultDict
import requests
from dataclasses import dataclass, field


@dataclass(init=False)
class WeatherProvider(ABC):
    api_key: str
    city: str
    country: str = field(default = None)
    state: str = field(default = None)


    @abstractmethod
    def get_api_url(self):
        pass

    def fetch(self):
        response = requests.get(self.get_api_url())
        return self.process(response.content)

    @abstractmethod
    def process( self, response ):
        pass

