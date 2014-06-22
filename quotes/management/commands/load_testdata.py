import sys
import datetime
from optparse import make_option

from django.core.management import BaseCommand

from quotes.models import Quote


class Command(BaseCommand):
    help = u'Loads some stub quotes for testing/development.'
    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            action='store_true',
            dest='force',
            default=False,
            help=u'Force loading by removing existing data.'),
        )

    def handle(self, *args, **kwargs):
        # If force, clean existing data.
        if kwargs['force']:
            sys.stdout.write(u'Deleting existing data!\n')
            Quote.objects.all().delete()

        # If quote objects exist, stop.
        if Quote.objects.count() > 0:
            raise Exception(u'Data already exists, will not load testdata, '
                            u'call with \'-f\' to clear existing data.')

        now = datetime.datetime.now()
        for i in xrange(100):
            created = now - datetime.timedelta(i)
            Quote.objects.create(
                id=i,
                created=created,
                quote='quote %s' % i)

        sys.stdout.write(u'Backend now contains %s quotes.\n' %
                         Quote.objects.count())
