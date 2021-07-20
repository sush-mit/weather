# weather
Python script for getting weather information for input location.  
_Please, refer to [ISO 3166](https://www.iso.org/obp/ui/#search) for the state codes or country codes._

## Arguments:
### General arguments:
    --city = City name.
    --state = State name.
    self.args_parse.add_argument('--country', type=str, metavar='', help='Country.')
    self.args_parse.add_argument('--name', type=str, metavar='', choices=lists.PROVIDERS+[None], help='Provider name.')
### Print arguements:
    self.args_parse.add_argument('-p', '--print', action='store_true', help='Print weather data to console.')
    self.args_parse.add_argument('--unit', type=str, metavar='', choices=lists.UNITS, help='Units to print temperature in.', default='K')
    self.args_parse.add_argument('--interval', type=float, metavar='', help='Interval to check weather (seconds).')
### Query arguments:
    self.args_parse.add_argument('--date', type=datetime.date.fromisoformat, metavar='', help='Date in YYYY-MM-DD.')
    self.args_parse.add_argument('--get', type=str, metavar='', choices=lists.GETABLE_COLUMN_NAMES, help='Data to get (can be comma separated values).', default='all')
    self.args_parse.add_argument('--timeframe',type=self.timeframe, metavar='', help='Time frame to get weather data from ("Ny"/"Nm"/"Nd").', default='1d')
    self.args_parse.add_argument('--orderby', type=self.column_names, metavar='', help='Order data by.', default='id')
    self.args_parse.add_argument('--orderin', type=str, metavar='', choices=lists.ORDER_IN, help='Order data in.', default='ASC')
    self.args_parse.add_argument('--max', action='store_true', help='Get maximum value of following argument.')
    self.args_parse.add_argument('--min', action='store_true', help='Get minimum value of following argument.')
    self.args_parse.add_argument('--temperature', type=self.timeframe, metavar='', help='Get minimum value of following argument.', default='1d')
    self.args_parse.add_argument('--humidity', type=self.timeframe, metavar='', help='Get minimum value of following argument.', default='1d')

    mutually_exclusive = self.args_parse.add_mutually_exclusive_group()

    mutually_exclusive.add_argument('--config', action='store_true', help='config api.')
    self.args_parse.add_argument('--key', type=str, metavar='', help='API Key.')
    mutually_exclusive.add_argument('--query', action='store_true', help='Get weather data from database.')
    mutually_exclusive.add_argument('-s', '--store', action='store_true', help='Store weather data in database.')
## Usage:
### Adding provider to config:
    $ python3 weather.py --config --name=<provider-name> --key=<api-key>
### Getting weather information:
    $ python3 weather.py --city=<city>
### Example:
    $ python3 weather.py --config --name=openweather --key=fwefa3r3a23aw
    Settings saved to config.ini.
    $ python3 weather.py --city Miami
    Temperature: 30.85C
    Humidity: 78%
    Weather condition: Clouds
