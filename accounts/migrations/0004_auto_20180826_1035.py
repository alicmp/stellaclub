# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-26 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180826_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.IntegerField(choices=[(0, '\u06a9\u0627\u0631\u0628\u0631 \u0639\u0627\u062f\u06cc'), (1, '\u0645\u063a\u0627\u0632\u0647')], default=0),
        ),
    ]
