import datetime

from django.db import models
from django.utils import timezone


class Quote(models.Model):
    created = models.DateTimeField(
        primary_key=True,
        default=timezone.make_aware(datetime.datetime.now(),
                                    timezone.get_default_timezone()))
    quote = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return '[%s, %s]' % (self.created, self.quote)

    class Meta:
        db_table = u'quotes'
