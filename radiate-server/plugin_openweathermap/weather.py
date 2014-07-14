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
CITY = 'Pirkkala,FI'

env = Environment(loader=PackageLoader(__name__, 'templates'))
template = env.get_template('template.html')


# Helper for fetching json from url. Always returns valid JSON.
def _get_json_data(url):
    try:
        result = requests.get(url)
        log.debug('From cache: %s' % result.from_cache)

        if result.status_code != 200:
            log.error("Server returned %s" % result.status_code)
            raise Exception("Server returned %s" % result.status_code)

        json_data = result.json()

    except Exception, err:
        log.error(err)
        json_data = {}

    return json_data

# Simplify weather data before presentation
def _enrich_weather_data(data):
    data['dt_time'] = str(datetime.fromtimestamp(data['dt']).strftime('%H:%M'))
    data['temp_avg'] = (data['main']['temp_max'] + data['main']['temp_min'])/2
    return data

# Return display-ready card in HTML
def get_card():

    try:
        CACHE_PATH = "cache_weather"
        if __name__ == "plugin_openweathermap.weather":
            CACHE_PATH = "plugin_openweathermap/cache_weather"
        requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=900)

        forecast_data = _get_json_data('http://api.openweathermap.org/data/2.5/forecast?q={0}&units=metric'.format(CITY))
        current_data = _get_json_data('http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric'.format(CITY))

        forecast_data['list'] = map(_enrich_weather_data, forecast_data['list'])
	current_data = _enrich_weather_data(current_data)

	# Remove past forecast
	if current_data['dt'] >= forecast_data['list'][0]['dt']:
            forecast_data['list'].pop(0)

        return template.render(current=current_data, forecast=forecast_data['list'][:8])

    except Exception, err:
        log.error(err)
        return "<h1>Card failed on top level</h1>"

if(__name__ == "__main__"):
    print get_card()
