# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0003_auto_20170226_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
