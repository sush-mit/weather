import datetime

class WeatherData:
    def __init__(self, temperature, humidity, weather):
        self.temperature = self.fix_float(temperature)
        self.converted_temperature = self.temperature
        self.humidity = self.fix_float(humidity)
        self.weather = weather
        self.date=datetime.date.today()
        self.time=datetime.datetime.now().time()

    def to_farenheit(self):
        self.converted_temperature = 1.8*(self.converted_temperature-273)+32
        self.converted_temperature = self.fix_float(self.converted_temperature)

    def to_celsius(self):
        self.converted_temperature -= 272.15
        self.converted_temperature = self.fix_float(self.converted_temperature)
    
    def fix_float(self, val):
        return float(f'{val:.2f}')
