# Radiate

![radiate](screenshot.png)

## Getting started

    sudo apt-get install pip
    sudo pip install -r requirements.txt
    cd radiate-api-server
    python apiserver.py

## Contributing

Pull requests, especially new plugins are welcome.

## Known issues

When using Flask's own debug web server, it is easy to get `error: [Errno 32] Broken pipe` with several requests. [The fix](http://stackoverflow.com/questions/12591760/flask-broken-pipe-with-requests) is to use a real WSGI server.
