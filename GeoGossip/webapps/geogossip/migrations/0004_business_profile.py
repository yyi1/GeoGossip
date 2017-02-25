# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 01:28
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geogossip', '0003_auto_20161103_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('categories', models.CharField(max_length=200)),
                ('is_closed', models.BooleanField()),
                ('image_url', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('display_phone', models.CharField(max_length=200)),
                ('review_count', models.IntegerField()),
                ('rating', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('age', models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('bio', models.TextField(blank=True, default='hey there', max_length=420)),
                ('picture', models.ImageField(blank=True, upload_to='add-user-photo')),
                ('follower', models.ManyToManyField(related_name='follow', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
