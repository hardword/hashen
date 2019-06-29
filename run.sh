#!/bin/bash

# I use gunicorn for concurrency purpose. You can change parameters according to your hardware capacity for better(or worse) performance
# Reference: http://docs.gunicorn.org/en/stable/settings.html
gunicorn --worker-class=gevent --worker-connections=1000 --workers=3 --pid gunicorn.pid --bind 0.0.0.0:8080 main:application
