def weather_data(weather, ap):
    print(f'\nTemperature: {weather.converted_temperature}{ap.unit.upper()}\nHumidity: {weather.humidity}%\nWeather condition: {weather.weather}')

def database_weather_data(data):
    print(data)