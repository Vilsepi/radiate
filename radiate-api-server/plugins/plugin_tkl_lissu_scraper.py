#!/usr/bin/env python
#
# Scrapes Lissu http://lissu.tampere.fi/
#

from yapsy.IPlugin import IPlugin
from bs4 import BeautifulSoup
from time import strftime
import requests
import requests_cache
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class LissuScrape(IPlugin):

    def __init__(self): 
        cache_path = "plugins/" + __name__
        requests_cache.install_cache(cache_path, backend='sqlite', expire_after=7200)
        log.debug("Installed cache")

    def _scrape_html_into_json(self, html_string):
        try:
            scraped_soup = BeautifulSoup(html_string)
            bus_stop_info = scraped_soup.tr.find_all("td")
            bus_stop_name = bus_stop_info[0].text[:-7]
            updated_at = bus_stop_info[1].text[4:]

            line_list = []

            # Note: There is a layout bug in Lissu's HTML so there should be 2 instead of 3 here in sublist
            # Lissu has an extra tr tag inside another tr which is not terminated
            for tr in scraped_soup.find_all("tr")[3:]:
                keys = tr.find_all("td")
                line_list.append({'line': keys[0].text, 'destination': keys[2].text, 'eta': [keys[3].text, keys[4].text]})

            return {'bus_stop_name': bus_stop_name, 'updated_at': updated_at, 'next_buses': line_list}
        except Exception, err:
            return json.dumps({"status":"err","message":"Failed to scrape source html"})

    def _get_data_for_bus_stop(self, stop_id):

        #try:
        source_url = "http://lissu.tampere.fi/monitor.php?stop=" + stop_id
        result = requests.get(source_url)
        log.debug("From cache: %s" % result.from_cache)

        if result.status_code == 200 and result.text:
            return self._scrape_html_into_json(result.text)
        else:
            log.error("Server returned %s" % result.status_code)
                #raise Exception("Server returned %s" % result.status_code)
        #except Exception, err:
        #   log.error(err)
        #  return json.dumps({"status":"err","message":"Getting data from source server failed"})

    def get_data(self, args):
        try:
            if args:
                if args.get('stops'):
                    bus_stops = [stop.strip() for stop in args.get('stops').split(',')]
                    bus_stops_data = map(self._get_data_for_bus_stop, bus_stops)
                    return json.dumps({"status": "ok", "stops": bus_stops_data})
            return json.dumps({"status": "err", "message": "Pass the bus stops as urls params"})
        except Exception, err:
            log.error(err)
            return json.dumps({"status": "err", "message": "Lissu plugin failed"})

if(__name__ == "__main__"):
    print get_data()
