# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Shop(models.Model):
  choices = (
		(0, 'کافی‌شاپ'),
		(1, 'سرگرمی'),
		(2, 'رستوران'),
    (3, 'سفره‌خانه'),
	)
  name              = models.CharField(max_length=1024)
  phone_number      = models.CharField(max_length=11)
  address           = models.TextField(blank=True, null=True)
  description       = models.TextField(blank=True, null=True)
  category          = models.IntegerField(choices=choices)
  image_name        = models.CharField(max_length=1024, null=True, blank=True)
  map_url           = models.URLField(max_length=1024, null=True, blank=True)
  def __unicode__(self):
    return self.name

class OwnerPhoneNumber(models.Model):
  shop              = models.ForeignKey(Shop)
  num               = models.CharField(max_length=11)
  def __unicode__(self):
    return self.shop.name

class Discount(models.Model):
  shop              = models.ForeignKey(Shop)
  percentage        = models.IntegerField()
  price             = models.FloatField(null=True, blank=True)
  is_expire         = models.BooleanField(default=False)
  start_date        = models.DateTimeField(null=True, blank=True)
  expiration_date   = models.DateTimeField(null=True, blank=True)

  def __unicode__(self):
    return "{} - {}".format(self.shop.name, self.percentage)