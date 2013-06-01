#!/usr/bin/env python
'''
A simple application that gets the quotes from the slashdot website
and puts them in the default database defined in the settings module.

The idea is to put this script in a crontab or similar.
'''

import os
import sys

# Bootstrap environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'slashdotdjango.settings'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from contextlib import closing
from HTMLParser import HTMLParser
import logging
import logging.handlers
import time

import requests

from quotes.models import Quote

LOGFILE = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'slashdotparser.log'))


class SlashdotParser(HTMLParser):
    '''
    A simple specialization of HTMLParser, that can find and log the quote of
    the slashdot website.
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_blockquote = False
        self.quote = None

    def handle_starttag(self, tag, _):
        if tag == 'blockquote':
            self.in_blockquote = True

    def handle_data(self, data):
        if self.in_blockquote and data:
            self.quote = data

    def handle_endtag(self, tag):
        if self.in_blockquote and tag == 'blockquote':
            self.in_blockquote = False


def get_slashdot_body():
    '''
    Returns the body from the slashdot website,
    if this fails en exception is thrown.

    :returns: Body of slashdot.org, as a string.
    '''

    result = None
    with closing(requests.get('http://slashdot.org/')) as r:
        if r.status_code == 200:
            return r.text
        else:
            logging.debug('Did not recieve a 200 OK')
            r.raise_for_status()


def parse_slashdot_body(body):
    '''
    Parses the html of slashdot.org's website and returns the quote
    contained on the website.

    :param body: Body of slashdot.org, as a string.
    :returns: The quote on the page, as a string.
    '''
    with closing(SlashdotParser()) as parser:
        parser.feed(body)
        return parser.quote


def save_quote_in_table(quote):
    '''
    Saves the quote specified in the database.

    Returns True if quote is saved, else False and logs the
    reason why it failed.

    :returns: True if the quote was saved, if it already existed False.
    '''
    newquote, created = Quote.objects.get_or_create(quote=quote)
    return created


def _setup_logging():
    '''
    Initializes logging for the application, this is usually done from the mail method.
    '''
    logging.basicConfig()
    logger = logging.getLogger()
    logger.addHandler(logging.handlers.TimedRotatingFileHandler(
        LOGFILE, 'midnight', 1, backupCount=7))
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.WARN)
    return logger


def main():
    '''
    Run the script.
    '''

    logger = _setup_logging()

    try:
        # get slashdot HTML.
        body = get_slashdot_body()

        # parse quote from the body.
        quote = parse_slashdot_body(body)

        # attempt to save the quote.
        if save_quote_in_table(quote):
            logger.info('saved new query')
        else:
            logger.info('quote already exists')

    except Exception, e:
        logger.error(e)
        raise

if __name__ == '__main__':
    main()
