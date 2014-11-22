from yapsy.IPlugin import IPlugin
from time import strftime
import json

class LissuScrape(IPlugin):
    def get_data(self, args):

		print args
        return json.dumps({"status":"ok","server_time": strftime("%Y-%m-%d %H:%M:%S")})
