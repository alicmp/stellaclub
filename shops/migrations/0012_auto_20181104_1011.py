# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-04 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0011_auto_20181027_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='category',
            field=models.IntegerField(choices=[(0, '\u06a9\u0627\u0641\u06cc\u200c\u0634\u0627\u067e'), (1, '\u0633\u0631\u06af\u0631\u0645\u06cc'), (2, '\u0631\u0633\u062a\u0648\u0631\u0627\u0646'), (3, '\u0633\u0641\u0631\u0647\u200c\u062e\u0627\u0646\u0647')]),
        ),
    ]
