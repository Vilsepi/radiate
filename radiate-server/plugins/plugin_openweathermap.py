#!/usr/bin/env python
#
# Uses OpenWeatherMap API http://openweathermap.org/API
# which is licensed under Creative Commons license http://creativecommons.org/licenses/by-sa/2.0/
# Requires an API key.

from yapsy.IPlugin import IPlugin
import logging
import requests
import requests_cache
import socket
import json
import plugin_openweathermap_secret as secret
from datetime import datetime
from jinja2 import Environment, PackageLoader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Specify cities here you wish to monitor
CITY = 'Tampere,FI'
REMOTE_API_BASE_URL = "http://api.openweathermap.org/data/2.5/"


class OpenWeatherMap(IPlugin):

    def __init__(self):
        cache_path = "plugins/" + __name__
        requests_cache.install_cache(cache_path, backend='memory', expire_after=600)
        log.debug("Installed cache")

    def _get_json_data(self, url):
        """ Helper for fetching json from url. Always returns valid JSON """

        json_data = {}
        try:
            result = requests.get(url)
            log.debug('From cache: %s' % result.from_cache)

            if result.status_code != 200:
                log.error("Server returned %s" % result.status_code)
                raise Exception("Server returned %s" % result.status_code)

            json_data = result.json()

        except requests.exceptions.ConnectionError, err:
            log.error(err)
        except Exception, err:
            log.error(err)
            raise err

        return json_data

    def _enrich_weather_data(self, data):
        """ Simplify weather data before presentation """

        data['dt_time'] = str(datetime.fromtimestamp(data['dt']).strftime('%H:%M'))
        data['temp_avg'] = (data['main']['temp_max'] + data['main']['temp_min'])/2
        return data

    def get_data(self, args):
        """ Return current weather and forecast in json, or json error object on error """

        try:
            forecast_data = self._get_json_data('{}forecast?q={}&units=metric&appid={}'.format(REMOTE_API_BASE_URL, CITY, secret.remote_api_key))
            current_data = self._get_json_data('{}weather?q={}&units=metric&appid={}'.format(REMOTE_API_BASE_URL, CITY, secret.remote_api_key))

            forecast_data['list'] = map(self._enrich_weather_data, forecast_data['list'])
            current_data = self._enrich_weather_data(current_data)

            # Remove past forecast
            #if current_data['dt'] >= forecast_data['list'][0]['dt']:
            #    forecast_data['list'].pop(0)

            return json.dumps({"status": "ok", "current": current_data, "forecast": forecast_data})

        except socket.gaierror, err:
            log.error(err)
            return json.dumps({"status": "error", "message": err})


if(__name__ == "__main__"):
    plugin = OpenWeatherMap()
    print plugin.get_data()
