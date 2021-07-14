# weather
Python script for getting weather information for input location.  
_Please, refer to [ISO 3166](https://www.iso.org/obp/ui/#search) for the state codes or country codes._
### Requirements:
```
mechanize==0.4.5
```
### Usage:
#### Adding a provider:
```
$ python3 weather.py --config --name=<provider_name> --key=<provider_key>
```
#### Getting weather information:
```
$ python3 weather.py --name=<provider_name> --city=<city>
```
### Example:
```
$ python3 weather.py --config --name=weatherapi --key=fwea86ftaewfah39faq3f
Settings saved to config.ini.
$ python3 weather.py --name=weatherapi --city=miami
Temperature: 25C
Humidity: 78%
Weather condition: Clouds
```
