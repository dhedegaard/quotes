# Slashdot Quotes #

The code behind my database of quotes from the bottom of the slashdot site.

A running version can be found here: http://sd.dhedegaard.dk/

### How to get it running ###

The project is implemented in python using django, so to get the code up and running you need the following.

- A database backend compatible with django.
- A webserver for running WSGI.
- Some sort of crontab for running the "getquote" command.