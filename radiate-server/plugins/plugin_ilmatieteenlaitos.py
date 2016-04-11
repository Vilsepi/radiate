#!/usr/bin/env python
#
# Uses Finnish Meteorological Institute API http://en.ilmatieteenlaitos.fi/open-data-manual
# which is licensed under Creative Commons license https://creativecommons.org/licenses/by/4.0/
# Requires an API key.

from yapsy.IPlugin import IPlugin
import logging
import requests
import requests_cache
import socket
import json
from xml.etree import ElementTree
import plugin_ilmatieteenlaitos_secret as secret
from datetime import datetime
from jinja2 import Environment, PackageLoader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

CITY = 'tampere'
REMOTE_API_BASE_URL = "http://data.fmi.fi/fmi-apikey/"

class Ilmatieteenlaitos(IPlugin):

    def __init__(self):
        cache_path = "plugins/" + __name__
        requests_cache.install_cache(cache_path, backend='memory', expire_after=240)
        log.debug("Installed cache")

    def _get_xml_data(self, url):
        """ Helper for fetching xml from url. """

        try:
            result = requests.get(url)
            log.debug('From cache: %s' % result.from_cache)

            if result.status_code != 200:
                log.error("Server returned %s" % result.status_code)
                raise Exception("Server returned %s" % result.status_code)

            root = ElementTree.fromstring(result.content)

        except requests.exceptions.ConnectionError, err:
            log.error(err)
        except Exception, err:
            log.error(err)
            raise err

        return root

    def _parse_xml_data(self, url):
        """ Helper for parsing xml from url. Always returns valid JSON """

        root = self._get_xml_data(url)
        ns = {
            'gml': 'http://www.opengis.net/gml/3.2',
            'gmlcov': 'http://www.opengis.net/gmlcov/1.0',
            'swe': 'http://www.opengis.net/swe/2.0'
        }

        assert len(root.findall(".//gmlcov:positions", ns)) == 1, "More than one gmlcov:positions found"
        assert len(root.findall(".//gml:doubleOrNilReasonTupleList", ns)) == 1, "More than one gml:doubleOrNilReasonTupleList found"
        assert len(root.findall(".//swe:DataRecord", ns)) == 1, "More than one swe:DataRecord found"

        forecast = []
        try:
            # Parse parameter names
            field_types = [field.attrib.get('name') for field in root.findall(".//swe:DataRecord", ns)[0]]

            # Parse forecast timestamps
            for line in root.findall(".//gmlcov:positions", ns)[0].text.splitlines():
                split_line = line.split()
                if len(split_line) == 3:
                    #data['dt_time'] = str(datetime.fromtimestamp(data['dt']).strftime('%H:%M'))
                    forecast.append({'Timestamp': int(split_line[2])})

            # Parse parameters for each forecast point in time
            forecast_index = 0
            for line in root.findall(".//gml:doubleOrNilReasonTupleList", ns)[0].text.splitlines():
                split_line = line.split()
                if len(split_line) == len(field_types):
                    for i, value in enumerate(split_line):
                        forecast[forecast_index][field_types[i]] = float(value)
                    forecast_index += 1

        except Exception, err:
            log.error(err)
            raise err

        return forecast

    def get_data(self, args):
        """ Return current weather and forecast in json, or json error object on error """

        try:
            forecast_data = self._parse_xml_data('{}{}/wfs?request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::multipointcoverage&place={}'.format(REMOTE_API_BASE_URL, secret.remote_api_key, CITY))
            #current_data = self._get_json_data('{}weather?q={}&units=metric&appid={}'.format(REMOTE_API_BASE_URL, CITY, secret.remote_api_key))
            current_data = {"msg": "not implemented"}

            return json.dumps({"status": "ok", "current": current_data, "forecast": forecast_data})

        except socket.gaierror, err:
            log.error(err)
            return json.dumps({"status": "error", "message": err})


if(__name__ == "__main__"):
    plugin = Ilmatieteenlaitos()
    print plugin.get_data(None)
