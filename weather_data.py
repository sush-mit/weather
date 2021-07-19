import datetime

class WeatherData:
    def __init__(self, temperature, humidity, weather):
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather
<<<<<<< HEAD
        if isinstance(self.temperature, float):
            self.temperature = self.fix_float(self.temperature)
        if isinstance(self.humidity, float):
            self.humidity = self.fix_float(self.humidity)

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
=======
        self.date=datetime.date.today()
        self.time=datetime.datetime.now().time()
>>>>>>> implemented database read
