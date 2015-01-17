#!/usr/bin/env python

from flask import Flask
from flask import request
from flask.ext.cors import CORS
from yapsy.PluginManager import PluginManager
import config
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

plugin_manager = PluginManager()
plugin_manager.setPluginPlaces(config.plugin_directories)
plugin_manager.collectPlugins()

for plugin in plugin_manager.getAllPlugins():
    if plugin.name in config.active_plugins:
        plugin_manager.activatePluginByName(plugin.name)
        print "Loaded plugin", plugin.name

app = Flask(__name__)
cors = CORS(app)

@app.route("/api/", methods=['GET'])
def list_active_plugins():
    plugins = []
    for plugin in plugin_manager.getAllPlugins():
        plugins.append(plugin.name)
    return json.dumps({"plugins":plugins})

@app.route("/api/<plugin>", methods=['GET'])
def call_plugin(plugin):
    if plugin in config.active_plugins:
        pluginInfo = plugin_manager.getPluginByName(plugin)
        if pluginInfo:
            return pluginInfo.plugin_object.get_data(request.args)
    return "Plugin {0} does not exist or is not active".format(plugin)

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return 'Try /api/test'

if(__name__ == "__main__"):
    app.run(host=config.app_host, port=config.app_port, debug=config.app_debug)