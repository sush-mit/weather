# weather
Python script for getting weather information for input location.  
_Please, refer to [ISO 3166](https://www.iso.org/obp/ui/#search) for the state codes or country codes._
### Requirements:
```
mechanize==0.4.5
```
### Usage:
```
$ python3 weather.py -ci <city> -s <state-code> -co <country-code>
```
### Example:
```
$ python3 weather.py -ci Kathmandu -s NP-BA -co NPL
Temperature: 299.34K
Humidity: 78%
Weather condition: Clouds
```
