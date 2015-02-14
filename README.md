# Slashdot Quotes #

[![Build Status](https://drone.io/bitbucket.org/dennishedegaard/quotes/status.png)](https://drone.io/bitbucket.org/dennishedegaard/quotes/latest)

The code behind my database of quotes from the bottom of the slashdot site.

A running version can be found here: http://sd.dhedegaard.dk/

### How to get it running ###

The project is implemented in python using django, so to get the code up and running you need the following.

- Install requirements: $ pip install -r requirements.txt
- Run $ manage.py runserver - or use uwsgi/apache with mod_wsgi or similar