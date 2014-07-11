#!/usr/bin/env python
#
# Uses OpenWeatherMap API http://openweathermap.org/API
# which is licensed under Creative Commons license http://creativecommons.org/licenses/by-sa/2.0/

import logging
import requests
import requests_cache
from datetime import datetime
from jinja2 import Environment, PackageLoader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Specify cities here you wish to monitor
CITY = 'Tampere,FI'

env = Environment(loader=PackageLoader(__name__, 'templates'))
template = env.get_template('template.html')


def _get_weather_for_city(location):

    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&units=metric' % location
        result = requests.get(url)
        log.debug('From cache: %s' % result.from_cache)

        if result.status_code != 200:
            log.error("Server returned %s" % result.status_code)
            raise Exception("Server returned %s" % result.status_code)

        weather_data = result.json()

    except Exception, err:
        log.error(err)
        weather_data = {}

    return weather_data

# Filter data
def _mangle_data(data):
    # TODO wtf these timezones are so messed up in openweather
    obj = {}
    obj['time'] = str(datetime.fromtimestamp(data['dt']).strftime('%H:%M'))
    obj['debug_time'] = data['dt_txt']
    obj['icon'] = data['weather'][0]['icon']
    obj['temp_min'] = data['main']['temp_min']
    obj['temp_avg'] = (data['main']['temp_max'] + data['main']['temp_min'])/2
    obj['temp_max'] = data['main']['temp_max']
    obj['text'] = data['weather'][0]['main']
    return obj


# Return display-ready card in HTML
def get_card():

    try:
        CACHE_PATH = "cache_weather"
        if __name__ == "plugin_openweathermap.weather":
            CACHE_PATH = "plugin_openweathermap/cache_weather"
        requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=900)

        weather_data = _get_weather_for_city(CITY)
	mangled_data = map(_mangle_data, weather_data['list'])
	location = weather_data['city']['name']

        return template.render(location=location, data=mangled_data[:8])

    except Exception, err:
        log.error(err)
        return "<h1>Card failed on top level</h1>"

if(__name__ == "__main__"):
    print get_card()
