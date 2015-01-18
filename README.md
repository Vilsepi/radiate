# Radiate

![radiate](screenshot.png)

## Getting started

### For the new, under-development version

    sudo apt-get install pip
    cd radiate-api-server/
    sudo pip install -r requirements.txt
    python apiserver.py

    cd radiate-web-client/
    python -m SimpleHTTPServer

### For the working legacy version

    sudo apt-get install pip
    cd legacy/radiate-server/
    sudo pip install -r requirements.txt
    python webserver.py

    sudo apt-get install google-chrome x11-xserver-utils, unclutter
    # allow all users to start X session
    sudo dpkg-reconfigure x11-common
    cd legacy/radiate-client/
    ./radiate-client.sh

For background service that start on server boot, check the upstart job examples.

## Contributing

Pull requests, especially new plugins are welcome.

## Known issues

When using Flask's own debug web server, it is easy to get `error: [Errno 32] Broken pipe` with several requests. [The fix](http://stackoverflow.com/questions/12591760/flask-broken-pipe-with-requests) is to use a real WSGI server.
