# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from accounts.models import User

from django.db import models

from shops.models import Shop

class Transaction(models.Model):
  transaction_id = models.IntegerField(unique=True)
  shop = models.ForeignKey(Shop)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
  user = models.ForeignKey(User)
  amount = models.FloatField()
  timestamp   = models.DateTimeField(auto_now_add=True)
  is_successful = models.BooleanField(default=False)

  def __unicode__(self):
    return "{} - {}".format(self.user, self.amount)

class Deposit(models.Model):
  user = models.ForeignKey(User)
  total = models.FloatField(default=0)

  def __unicode__(self):
    return "{}: {}".format(self.user, self.total)

class Checkout(models.Model):
  status_choices = (
    (0, 'درخواست تسویه حساب ارسال شده'),
    (1, 'تسویه حساب در حال انجام'),
    (2, 'تسویه حساب انجام شده')
  )
  user = models.ForeignKey(User)
  amount = models.FloatField()
  requested_date = models.DateTimeField(auto_now_add=True)
  settle_date = models.DateTimeField(null=True, blank=True)
  is_settled = models.BooleanField(default=False)
  status = models.IntegerField(choices=status_choices, default=0)

  def __unicode__(self):
    return self.user.full_name