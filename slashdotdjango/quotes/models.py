from django.db import models
from datetime import datetime
import time

class Quote(models.Model):
    created = models.DateTimeField(primary_key=True, default=datetime.now())
    quote = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return '[%s, %s]' % (self.created, self.quote)

    class Meta:
        db_table = u'quotes'
