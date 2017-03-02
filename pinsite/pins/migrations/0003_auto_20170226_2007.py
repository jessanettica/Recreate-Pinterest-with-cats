# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0002_auto_20170226_0657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pin',
            old_name='pin_id',
            new_name='pinterest_id',
        ),
    ]
