#!/usr/bin/env python
#
# Uses Lissu http://lissu.tampere.fi/
#

import logging
import requests
import requests_cache
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Specify bus stops here you wish to monitor
BUS_STOPS = ['3733', '3523','3737']

env = Environment(loader=PackageLoader(__name__, 'templates'))
template = env.get_template('template.html')


def _get_data_for_bus_stop(stop_id):

    try:
        url = "http://lissu.tampere.fi/monitor.php?stop=" + stop_id
        result = requests.get(url)
        log.debug("From cache: %s" % result.from_cache)

        if result.status_code != 200:
            log.error("Server returned %s" % result.status_code)
            raise Exception("Server returned %s" % result.status_code)

        scraped_soup = BeautifulSoup(result.text)

        stop_info = scraped_soup.tr.find_all("td")
        stop_name = stop_info[0].text[:-7]
        updated_at = stop_info[1].text[4:]

        line_list = []

        # TODO There is a layout bug in Lissu's HTML so there should be 2 instead of 3 here in sublist
        # Lissu has an extra tr tag inside another tr which is not terminated
        for tr in scraped_soup.find_all("tr")[3:]:
            keys = tr.find_all("td")
            # TODO compare busline for list of favorites and add favorite boolean to dict
            line_list.append({'line': keys[0].text, 'destination': keys[2].text, 'eta1': keys[3].text, 'eta2': keys[4].text})

    except Exception, err:
        log.error(err)
        stop_name = 'Stop ID ' + stop_id
        updated_at = '-'
        line_list = {'line': 'ERR', 'destination': 'Error', 'eta1': '', 'eta2': ''}

    return {'stop_name': stop_name, 'updated_at': updated_at, 'next_buses': line_list}


# Return display-ready card in HTML
def get_card():

    try:
        CACHE_PATH = "cache_lissu"
        if __name__ == "plugin_lissuscraper.lissu":
            CACHE_PATH = "plugin_lissuscraper/cache_lissu"
        requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=15)

        bus_stops_data = map(_get_data_for_bus_stop, BUS_STOPS)

        return template.render(data=bus_stops_data)
    except Exception, err:
        log.error(err)
        return "<h1>Card failed on top level</h1>"

if(__name__ == "__main__"):
    print get_card()
