import logging
from contextlib import closing
from HTMLParser import HTMLParser
from django.db.transaction import commit_on_success

import requests
from django.core.management import BaseCommand

from quotes.models import Quote

logger = logging.getLogger(__name__)


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

    :returns: Quote-object and a bool, telling if it's been created or not.
    '''
    return Quote.objects.get_or_create(quote=quote)


@commit_on_success
def main():
    # get slashdot HTML.
    body = get_slashdot_body()

    # parse quote from the body.
    quote = parse_slashdot_body(body)

    # attempt to save the quote.
    quote, created = save_quote_in_table(quote)
    if created:
        logger.info('saved new query (id=%s)', quote.pk)
    else:
        logger.info('quote already exists (id=%s)', quote.pk)


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()