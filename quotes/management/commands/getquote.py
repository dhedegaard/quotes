import logging
from contextlib import closing
from django.db import transaction

import requests
from bs4 import BeautifulSoup as BS
from django.core.management import BaseCommand

from quotes.models import Quote

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        # get HTML.
        with closing(requests.get('http://slashdot.org/',
                                  timeout=10)) as req:
            req.raise_for_status()
            body = req.text

        # Get quote from the body.
        soup = BS(body, 'html.parser')
        quote = soup.find('blockquote').p.text

        # Save the quote, if it does not already exist.
        quote, created = Quote.objects.get_or_create(quote=quote)
        if created:
            logger.info('saved new query (id=%s)', quote.pk)
        else:
            logger.info('quote already exists (id=%s)', quote.pk)
