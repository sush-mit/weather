class ArgsData:
    def __init__(self, city, state, country, name, key,
                    unit, interval,
                    date, get, timeframe, orderby, orderin, max, min, temperature, humidity,
                    config, query, print, store,
                    search_terms, filter_options):
        self.city = city
        self.state = state
        self.country = country
        self.name = name
        self.key = key

        self.unit = unit
        self.interval = interval

        self.date = date
        self.get = get
        self.timeframe = timeframe
        self.orderby = orderby
        self.orderin = orderin
        self.max = max
        self.min = min
        self.temperature = temperature
        self.humidity = humidity
        
        self.config = config
        self.query = query
        self.store = store
        self.print = print

        self.search_terms = search_terms
        self.filter_options = filter_options
