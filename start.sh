#!/bin/bash

PATH="/usr/bin:/usr/sbin"

source /home/django-app/.virtualenv/bin/activate

/home/django-app/code/manage.py runserver 0.0.0.0:${PORT}
