# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_id', models.PositiveIntegerField(null=True, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('url', models.CharField(default=b'', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, blank=True)),
                ('provider_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('buyable_product', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.TextField(default=b'', blank=True)),
                ('pin_id', models.PositiveIntegerField(null=True, blank=True)),
                ('img_url', models.CharField(default=b'', max_length=255, blank=True)),
                ('img_height', models.PositiveIntegerField(default=236, null=True, blank=True)),
                ('like_count', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('repin_count', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('boards', models.ManyToManyField(related_name='pins', to='pins.Board', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='img_url',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pin_user_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pin',
            name='pinner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
