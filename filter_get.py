import printer

def filter_get(database_data, ap):
    if ap.get == 'all':
        for data in database_data:
            data = [str(d) for d in data.__dict__.values()]
            data = ' '.join(data)
            printer.database_weather_data(data)
    if ap.get == 'temperature':
        for data in database_data:
            printer.database_weather_data(data.temperature)
    if ap.get == 'humidity':
        for data in database_data:
            printer.database_weather_data(data.humidity)
    if ap.get == 'weather':
        for data in database_data:
            printer.database_weather_data(data.weather)
    if ap.get == 'date':
        for data in database_data:
            printer.database_weather_data(data.date)