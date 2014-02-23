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
CITIES = ['Tampere,FI']

env = Environment(loader=PackageLoader(__name__, 'templates'))
template = env.get_template('template.html')


def _get_weather_for_city(location):

    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric' % location
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


# Return display-ready card in HTML
def get_card():

    try:
        CACHE_PATH = "cache_weather"
        if __name__ == "plugin_openweathermap.weather":
            CACHE_PATH = "plugin_openweathermap/cache_weather"
        requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=600)

        weather_data = map(_get_weather_for_city, CITIES)

        # TODO: This currently shows the same info for all cities as the first city
        updated_at = str(datetime.fromtimestamp(weather_data[0]['dt']).strftime('%H:%M'))
        sunrise = str(datetime.fromtimestamp(weather_data[0]['sys']['sunrise']).strftime('%H:%M'))
        sunset = str(datetime.fromtimestamp(weather_data[0]['sys']['sunset']).strftime('%H:%M'))

        return template.render(data=weather_data, updated_at=updated_at, sunrise=sunrise, sunset=sunset)
    except Exception, err:
        log.error(err)
        return "<h1>Card failed on top level</h1>"

if(__name__ == "__main__"):
    print get_card()
