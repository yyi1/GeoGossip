# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 00:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geogossip', '0005_auto_20161119_0142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geogossip.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='business',
            name='categories',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='display_phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='image_url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='review_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
