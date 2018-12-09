# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-22 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0007_auto_20181021_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='map_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]