#!/usr/bin/env python

from flask import Flask
import plugin_lissuscraper.lissu as lissu
import plugin_openweathermap.weather as weather
import plugin_test.test as test

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def root():
    return app.send_static_file('dashboard.html')


@app.route("/api/getCard/<card_name>")
def api_get_card(card_name):
    if card_name == "lissuscraper":
        return lissu.get_card()
    elif card_name == "openweathermap":
        return weather.get_card()
    elif card_name == "test":
        return test.get_card()
    else:
        return "Could not serve card {0}".format(card_name)

if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=9000, debug=True)
