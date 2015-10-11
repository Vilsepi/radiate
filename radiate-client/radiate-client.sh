#!/bin/sh
#
# Prerequisites:
# - google-chrome (or chromium-browser), x11-xserver-utils, unclutter
# - Run dpkg-reconfigure x11-common and allow all users to start X session
#   or alternatively start the xinit with sudo
#

default_url="http://localhost:8000"
resolution="1366,768"
browser_path="/usr/bin/google-chrome"

if [ -z "$1" ]; then
    echo "URL parameter was not given, using default URL $url"
    url=$default_url
else
    url=$1
    echo "Launching $URL"
fi

old_browser_pid=`ps au |grep "xinit $browser_path"|grep -v grep|awk '{print $2}'`

if [ -z "$old_browser_pid"]; then
    echo "No old process found"
else
    echo "Killing old instance with PID $old_browser_pid"
    `kill $old_browser_pid`
    sleep 3
fi

# Start browser UI
xinit $browser_path --kiosk --disable-translate --window-size=$resolution --app="$url"

