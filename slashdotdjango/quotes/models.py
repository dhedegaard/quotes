from django.db import models
import time

class Quote(models.Model):
    created = models.DateTimeField(primary_key=True)
    quote = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return '[%s, %s]' % (self.created, self.quote)

    class Meta:
        db_table = u'quotes'
