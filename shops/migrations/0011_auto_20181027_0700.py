# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-27 07:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0010_auto_20181027_0659'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopOwnerPhoneNumber',
            new_name='OwnerPhoneNumber',
        ),
    ]
