# weather
Python script for getting weather information for input location.
_Please, refer to [ISO 3166](https://www.iso.org/obp/ui/#search) for the state codes or country codes._
### Usage:
#### Adding provider to config:
```
$ python3 weather.py --config --name=<provider-name> --key=<api-key>
```
#### Getting weather information:
```
<<<<<<< HEAD
<<<<<<< HEAD
$ python3 weather.py --city=<city>
=======
$ python3 weather.py --name=<provider-name> --city=<city>
>>>>>>> Updated README.md, added unit checking.
=======
$ python3 weather.py --name=<provider-name> --city=<city>
>>>>>>> Updated README.md, added unit checking.
```
### Example:
```
$ python3 weather.py --config --name=openweather --key=fwefa3r3a23aw
Settings saved to config.ini.
<<<<<<< HEAD
<<<<<<< HEAD
$ python3 weather.py --city Miami
=======
$ python3 weather.py --name openweather --city Miami
>>>>>>> Updated README.md, added unit checking.
=======
$ python3 weather.py --name openweather --city Miami
>>>>>>> Updated README.md, added unit checking.
Temperature: 30.85C
Humidity: 78%
Weather condition: Clouds
```
