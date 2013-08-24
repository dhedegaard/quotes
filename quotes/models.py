import datetime

from django.db import models
from django.utils import timezone


class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(
        null=False,
        auto_now_add=True,)
    quote = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return '[%s, %s, %s]' % (self.id, self.created, self.quote)

    class Meta:
        db_table = u'quotes'
