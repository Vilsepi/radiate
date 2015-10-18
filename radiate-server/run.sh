#!/bin/sh

gunicorn -w 4 --timeout=600 --log-level=INFO apiserver:app
