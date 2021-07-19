import datetime

class WeatherData:
    def __init__(self, temperature, humidity, weather):
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather
        self.date=datetime.date.today()
        self.time=datetime.datetime.now().time()