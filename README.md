# Slashdot Quotes #

[![Build Status](https://travis-ci.org/dhedegaard/quotes.svg?branch=master)](https://travis-ci.org/dhedegaard/quotes)
[![Coverage Status](https://coveralls.io/repos/dhedegaard/quotes/badge.svg?branch=master)](https://coveralls.io/r/dhedegaard/quotes?branch=master)
[![Requirements Status](https://requires.io/github/dhedegaard/quotes/requirements.svg?branch=master)](https://requires.io/github/dhedegaard/quotes/requirements/?branch=master)

The code behind my database of quotes from the bottom of the slashdot site.

### How to get it running ###

The project is implemented in python using django, so to get the code up and running you need the following.

- Install requirements: $ pip install -r requirements.txt
- Run $ manage.py runserver - or use uwsgi/apache with mod_wsgi or similar
