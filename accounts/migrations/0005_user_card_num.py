# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-26 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180826_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='card_num',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
