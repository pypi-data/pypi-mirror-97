#!/bin/bash


# django
python manage.py makemessages -e txt -e html -e py --no-wrap --no-obsolete --no-default-ignore -a # -v 2

# js
python manage.py makemessages -d djangojs -e vue -e js --no-wrap --no-obsolete --no-default-ignore -a # -v 2
