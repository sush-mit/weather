import printer

def filter_get(database_data, ap):
    if ap.args.get == 'all':
        for data in database_data:
            data = [str(d) for d in data.__dict__.values()]
            data = ' '.join(data)
            printer.database_weather_data(data)
    if ap.args.get == 'temperature':
        for data in database_data:
            printer.database_weather_data(data.temperature)
    if ap.args.get == 'humidity':
        for data in database_data:
            printer.database_weather_data(data.humidity)
    if ap.args.get == 'weather':
        for data in database_data:
            printer.database_weather_data(data.weather)
    if ap.args.get == 'date':
        for data in database_data:
            printer.database_weather_data(data.date)