# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-27 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_transaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]