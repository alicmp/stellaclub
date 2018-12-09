# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Transaction)
admin.site.register(Deposit)
admin.site.register(Checkout)
