# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-23 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_checkout_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checkout',
            name='settle_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
