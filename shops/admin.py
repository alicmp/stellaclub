# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Shop, Discount, OwnerPhoneNumber

admin.site.register(Shop)
admin.site.register(Discount)
admin.site.register(OwnerPhoneNumber)
