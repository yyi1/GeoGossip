# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geogossip', '0004_business_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='business',
            name='lon',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
