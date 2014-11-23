#!/usr/bin/env python

from yapsy.IPlugin import IPlugin
from bs4 import BeautifulSoup
import datetime
import requests
import requests_cache
import json
import logging
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class LissuScrape(IPlugin):
    """ Scrapes Lissu http://lissu.tampere.fi/ """

    def __init__(self): 
        cache_path = "plugins/" + __name__
        requests_cache.install_cache(cache_path, backend='sqlite', expire_after=7200)
        log.debug("Installed cache")

    def _get_minutes_until_time(self, time_string):
        """ Takes a time as hh:mm string and calculates time left in minutes until time is reached """
        # TODO time zones and summer time :(

        now = datetime.datetime.now()
        time_string_split = time_string.split(':')
        upcoming = now.replace(hour=int(time_string_split[0]), minute=int(time_string_split[1]), second=0, microsecond=0)

        if upcoming < now:
            upcoming += datetime.timedelta(days=1)
        time_left = upcoming - now

        return time_left.seconds/60

    def _enrich_estimate(self, time_string):
        """ Unify Lissu times which can be in '13 min', '07:33' or '07:33z' format"""
        
        time_object = {'source_time': time_string}
        try:
            time_schedule = re.search('\d\d:\d\d', time_string)
            if time_schedule:
                time_object['is_tracked'] = False
                time_object['time'] = time_schedule.group(0)
                time_object['estimate_minutes'] = self._get_minutes_until_time(time_schedule.group(0))
            else:
                time_estimate = re.search('(\d+) min', time_string)
                if time_estimate:
                    time_object['is_tracked'] = True
                    time_object['estimate_minutes'] = time_estimate.group(1)
        except IndexError:
            log.error("Failed to parse times")

        return time_object

    def _scrape_html_into_json(self, html_string):
        #try:
            scraped_soup = BeautifulSoup(html_string)
            bus_stop_info = scraped_soup.tr.find_all("td")
            bus_stop_name = bus_stop_info[0].text[:-7]
            updated_at = bus_stop_info[1].text[4:]

            line_list = []

            # Note: There is a layout bug in Lissu's HTML so there should be 2 instead of 3 here in sublist
            # Lissu has an extra tr tag inside another tr which is not terminated
            for tr in scraped_soup.find_all("tr")[3:]:
                keys = tr.find_all("td")
                line_list.append({'line': keys[0].text, 'destination': keys[2].text, 'eta': map(self._enrich_estimate, [keys[3].text, keys[4].text])})

            return {'bus_stop_name': bus_stop_name, 'updated_at': updated_at, 'next_buses': line_list}
        #except Exception, err:
        #    return json.dumps({"status":"err","message":"Failed to scrape source html"})

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
