# About
Python script for getting weather information for input location. And storing them in a database.  
_Please, refer to [ISO 3166](https://www.iso.org/obp/ui/#search) for the state codes or country codes._
# **Arguments**
### General arguments
    --city                  City name.
    --state                 State name.
    --country               Country name.
    --name                  Provider name.

### Print arguements
    -p, --print:            Use to print weather data to console.
    --unit:                 Units to print temperature in.
                            choices = ['K', 'F', 'C']
                            default = K
    --interval:             Interval to check weather (seconds). Optional.
    --city:                 Required.
    --state, --country:     Optional.
### Database arguments
    -s, --store:            Use to store weather data in database.
    --query:                Use to get weather data from database.
                            accepts: --get, --city, --date, --timeframe, --orderby,
                            --orderin --max, --min, --temperature, --humidity, --min,
                            --timeframe
    --date:                 Date to query for.
                            input format = YYYY-MM-DD
    --get:                  Data to get.
                            choices = ['temperature', 'humidity', 'weather', 'date',
                            'all']
                            default = 'all'
    --timeframe:            Time frame to get weather data from.
                            input format = '1d', '1w', '1m', '1y'
    --orderby:              Order data by.
                            choices = ['id', 'city', 'temperature', 'humidity',
                            'weather', 'date', 'time']
                            default = 'id'
    --orderin:              Order data in.
                            choices = ['ASC', 'DSC']
                            default = 'ASC'
    --max:                  Use to get maximum value of following argument. (Doesn't
                            work with --timeframe.)
    --min:                  Use to get minimum value of following argument. (Doesn't
                            work with --timeframe.)
    --temperature:          Use after --max or --min, get max/min temperature value of
                            the last * timeframe. (doesn't work without --max/--min.)
                            input format = '1d', '1w', '1m', '1y'
    --humidity:             Use after --max or --min, get max/min humidity value of
                            the last * timeframe. (doesn't work without --max/--min.)
                            input format = '1d', '1w', '1m', '1y'

### Config arguments
    --config:               Use to set api configurations.
                            accepted arguments: --name, --key
    --key:                  API Key.
<br/>

# **Usage**:
## Adding provider to config
    # Add "fwefa3r3a23aw" as key for openweather
    $ python3 weather.py --config --name=openweather --key=fwefa3r3a23aw

<br/>

## Getting weather information
    # Print weather information for Miami on console every 2 seconds.
    $ python3 weather.py -p --city Miami --state US-FL --country US --interval 2

<br/>

## Storing weather information to database
    # Store weather information for Miami in database every 2 seconds.
    $ python3 weather.py -s --city Miami --state US-FL --country US --interval 2

<br/>

## Querying database
### Getting data for last N days
    # Print all stored weather information of the past two days for the city of Miami.
    $ python3 weather.py --query --get all --city miami --timeframe 2d
### Getting max temperature data for last N days
    # Print all stored weather information where the temperature is the highest in the last two days for the city of Miami.
    $ python3 weather.py --query --get all --city miami --max --temperature 2d