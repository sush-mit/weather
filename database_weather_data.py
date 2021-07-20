class DatabaseWeatherData:
    def __init__(self, id_, city, state, country, temperature, humidity, weather, date, time):
        self.id_ = id_
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather
        self.date = date
        self.time = time