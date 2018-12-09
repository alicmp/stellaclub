# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-21 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_auto_20181021_1423'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0007_auto_20181021_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender',
        ),
        migrations.AddField(
            model_name='transaction',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shops.Shop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]