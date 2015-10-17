#!/bin/bash

export DISPLAY=':0.0'
sleep 1

USAGE="See switch-case in script for possible argument"

case $1 in
  'refresh')
    xdotool keydown shift key F5; sleep 2; xdotool keyup shift
    ;;
  'zoom-in')
    xdotool keydown ctrl key plus; sleep 2; xdotool keyup ctrl
    ;;
  *)
    echo $USAGE
    ;;
esac
