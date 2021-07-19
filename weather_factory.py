from openweather import OpenWeather
from weatherapi import WeatherAPI
from weatherbit import WeatherBit

class WeatherProviderFactory:
    def get(self, provider):
        if provider == 'openweather':
            return OpenWeather()
        elif provider == 'weatherapi':
            return WeatherAPI()
        elif provider == 'weatherbit':
            return WeatherBit()