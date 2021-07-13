import sys
import mechanize
import json
import argparse

def get_weather(city, country, state):

    api_key = 'a85e593a075e92f3b7285c21b42811ae'
    location = ''

    if city == None and country == None and state == None:
        sys.exit('Not enough arguments.')
    if city != None:
        location += city
        if state != None:
            location += f',{state}'
        if country != None:
            location += f',{country}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
    try:
        res = mechanize.urlopen(url)
    except mechanize.HTTPError as e:
        if e.getcode() == 404:
            sys.exit(f'city/state/country "{location}" not found.')

    read = res.read()
    temp = int(json.loads(read)['main']['temp'])
    temp -= 272.15
    if isinstance(temp, float):
        temp = f'{temp:.2f}'
    humidity = json.loads(read)['main']['humidity']
    if isinstance(humidity, float):
        humidity = f'{humidity:.2f}'
    weather = json.loads(read)['weather'][0]['main']

    return (temp, humidity, weather)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Get weather of given location.')
    parser.add_argument('-ci', '--city', type=str, metavar='', help='Input name of city.')
    parser.add_argument('-s', '--state', type=str, metavar='', help='Input code of state.')
    parser.add_argument('-co', '--country', type=str, metavar='', help='Input code of country.')
    args = parser.parse_args()

    weather = get_weather(args.city, args.state, args.country)
    print(f'Temperature: {weather[0]}C\nHumidity: {weather[1]}%\nWeather condition: {weather[2]}')
