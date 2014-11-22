from yapsy.IPlugin import IPlugin
from time import strftime
import json

class Test(IPlugin):
    def get_data(self):
        return json.dumps({"status":"ok","server_time": strftime("%Y-%m-%d %H:%M:%S")})
