# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('quote', models.TextField(max_length=512, db_index=True)),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'quotes',
            },
            bases=(models.Model,),
        ),
    ]
