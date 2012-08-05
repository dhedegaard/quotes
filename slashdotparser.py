#!/usr/bin/env python
'''
A simple application that gets the quotes from the slashdot website
and puts them in a relational database.

By default the application will attempt to get a quote and then
sleep for SLEEP_TIME_SECONDS before trying again. Feel free to
change this constant to whatever you like.
'''

SLEEP_TIME_SECONDS = 60 * 10

DBNAME = 'slashdot'
DBUSER = 'slashdot'

import httplib
import psycopg2
import HTMLParser
import logging
import time

__author__ = 'Dennis Hedegaard'
__version__ = 0.1

class SlashdotParser(HTMLParser.HTMLParser):
    '''
    A simple specialization of HTMLParser, that can find and log the quote of
    the slashdot website.
    '''
    in_blockquote = False
    quote = None

    def handle_starttag(self, tag, _):
        if tag == 'blockquote':
            self.in_blockquote = True

    def handle_data(self, data):
        if self.in_blockquote and data:
            self.quote = data.strip()

    def handle_endtag(self, tag):
        if self.in_blockquote and tag == 'blockquote':
            self.in_blockquote = False

def get_slashdot_body(logger):
    '''
    Returns the body from the slashdot website,
    if this fails None is returned, else the body.
    '''
    result = None
    try:
        con = httplib.HTTPConnection('slashdot.org')
        con.connect()
        con.request('GET', '/')
        resp = con.getresponse()
        result = resp.read()
    except httplib.HTTPException, error:
        result = None
        logger.debug('Unable to get slashdot body because: %s'
                     % error)
    finally:
        resp.close()
        con.close()
    return result

def parse_slashdot_body(logger, body):
    '''
    Parses the html of slashdot.org's website and returns the quote
    contained on the website.
    '''
    parser = SlashdotParser()
    try:
        parser.quote = None
        parser.feed(body)
        parser.close()
        return parser.quote
    except HTMLParser.HTMLParseError, error:
        logger.debug('Unable to parse quote from body, because: %s' % error)
        return None

def save_quote_in_table(logger, quote, dbname=DBNAME, dbuser=DBUSER):
    '''
    Saves the quote specified in the database.

    Returns True if quote is saved, else False and logs the
    reason why it failed.
    '''
    conn = psycopg2.connect('dbname=%(dbname)s user=%(dbuser)s' % {
            'dbname': dbname,
            'dbuser': dbuser,
            })
    cur = conn.cursor()
    try:
        query = 'INSERT INTO quotes(quote) VALUES(%(quote)s)'
        cur.execute(query, {
                'quote': quote,
                })
        conn.commit()
    except psycopg2.IntegrityError, error:
        conn.rollback()
        # pgcode 23505 is unique key constraint on table column.
        if error.pgcode != '23505':
            logger.error('psycopg2.IntegrityError pgcode: %s' % error.pgcode)
        return False
    finally:
        cur.close()
        conn.close()
    return True

class SlashdotLogHandler(logging.StreamHandler):
    '''
    A simple log handler that emits the message of the record
    with date and time in front. As in:

    [YY-MM-DD hh-mm-ss] message
    '''
    def emit(self, record):
        print '[%s]: %s' % (time.strftime('%Y-%m-%d %T'), record.getMessage())

def main(sleeptime=SLEEP_TIME_SECONDS):
    '''
    This function starts the main loop. Run this to run the application.

    When the method is called, a loop runs forever.
    '''
    logger = logging.Logger('slashdot-parser')
    logger.addHandler(SlashdotLogHandler())

    while True:
        logger.debug('connecting to slashdot..')

        try:
            # get slashdot HTML.
            body = get_slashdot_body(logger)
            if body == None:
                continue
            # parse quote from the body.
            quote = parse_slashdot_body(logger, body)
            if quote == None:
                continue
            logger.debug('\tquote: %s' % quote)
            # attempt to save the quote.
            saved = save_quote_in_table(logger, quote)
            if saved:
                logger.info('\tNew quote saved: %s' % quote)
            else:
                logger.info('\tQuote already in the table.')
        except Exception, error:
            logger.error('\tUncaught exception(%s): %s' %
                         (error.__class__.__name__, error))

        logger.info('sleeping...')
        time.sleep(sleeptime)

if __name__ == '__main__':
    main(10)
