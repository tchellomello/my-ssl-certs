#!/bin/bash

PATH="/usr/bin:/usr/sbin"

/home/django-app/code/manage.py runserver 0.0.0.0:${PORT}
