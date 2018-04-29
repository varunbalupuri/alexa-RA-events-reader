BASE_URL = 'https://www.residentadvisor.net/events/{}/{}/day/{}'

DEFAULT_COUNTRY = 'uk'
DEFAULT_REGION = 'london'

# maximum number of events to read out
MAXIMUM_EVENTS = 5

# optional dict of form {'city' : list[venues]} for preferred venues
# these will be prioritised in event selection where possible.
WHITELIST = {'london': ['the yard',
                        'corsica studios',
                        'bloc (autumn street)',
                        'steelyard',
                        'studio spaces e2',
                        'brewhouse',
                        'bunker club',
                        "canavan's peckham",
                        "clf arts cafe",
                        "clf art cafe [block a, bussey building]"]
            }

