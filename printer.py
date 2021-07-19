def weather_data(weather, ap):
    print(f'\nTemperature: {weather.temperature}{ap.args.unit.upper()}\nHumidity: {weather.humidity}%\nWeather condition: {weather.weather}')

def database_weather_data(data):
    print(data)