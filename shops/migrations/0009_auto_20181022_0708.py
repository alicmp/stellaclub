# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-22 07:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0008_auto_20181022_0655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='image',
            new_name='image_name',
        ),
    ]