import datetime

class WeatherData:
    def __init__(self, temperature, humidity, weather):
        self.temperature = self.fix_float(temperature)
        self.humidity = self.fix_float(humidity)
        self.weather = weather
        self.date=datetime.date.today()
        self.time=datetime.datetime.now().time()

    def to_farenheit(self):
        self.temperature = 1.8*(self.temperature-273)+32
        if isinstance(self.temperature, float):
            self.temperature = self.fix_float(self.temperature)

    def to_celsius(self):
        self.temperature -= 272.15
        if isinstance(self.temperature, float):
            self.temperature = self.fix_float(self.temperature)
    
    def fix_float(self, val):
        return float(f'{val:.2f}')
