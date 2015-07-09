from __future__ import unicode_literals
from django.db import models


class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(
        null=False, auto_now_add=True, db_index=True)
    quote = models.TextField(max_length=512, db_index=True)

    def __unicode__(self):
        return '[%s, %s, %s]' % (self.id, self.created, self.quote)

    class Meta:
        db_table = 'quotes'
        ordering = ('-id', )
