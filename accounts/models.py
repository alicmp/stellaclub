# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import (
		AbstractBaseUser, BaseUserManager
)
from django.utils import timezone

from django.db import models

import random

class UserManager(BaseUserManager):
	def create_user(self, 
		phone_number, 
		username=None,
		email=None, 
		full_name=None, 
		password=None, 
		is_active=True, 
		is_staff=False, 
		is_admin=False,
		expire=None):
		if not phone_number:
			raise ValueError("Users must have a phone number")
		user_obj = self.model(
			phone_number = phone_number,
		)
		if not password:
			user_obj.set_unusable_password()
		else:
			user_obj.set_password(password) # change user password
		if not expire:
			user_obj.expire = timezone.now() + timezone.timedelta(minutes=2)
		else:
			user_obj.expire = expire
		user_obj.full_name = full_name
		user_obj.email = email
		user_obj.username = username
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, phone_number, username=None, email=None, full_name=None, password=None):
		user = self.create_user(
			email=email,
			username=username,
			phone_number=phone_number,
			full_name=full_name,
			password=password,
			is_staff=True
		)
		return user

	def create_superuser(self, phone_number, password, username=None, email=None, full_name=None):
		user = self.create_user(
			email=email,
			username=username,
			phone_number=phone_number,
			full_name=full_name,
			password=password,
			is_staff=True,
			is_admin=True,
		)
		return user

	def new_or_get(self, phone_number):
		qs = self.get_queryset().filter(phone_number=phone_number)
		random_password = create_random_password()
		if qs.count() == 1:
			user_obj = qs.first()
		else:
			user_obj = User(phone_number=phone_number)
		user_obj.set_password(random_password)
		user_obj.expire = timezone.now() + timezone.timedelta(minutes=2)
		user_obj.save()
		return user_obj, random_password


class User(AbstractBaseUser):
	phone_number = models.CharField(max_length=17, unique=True)
	username     = models.CharField(max_length=255, unique=True, blank=True, null=True)
	email        = models.EmailField(max_length=255, unique=True, blank=True, null=True)
	full_name    = models.CharField(max_length=255, blank=True, null=True)
	card_num     = models.CharField(max_length=16, null=True, blank=True)
	active       = models.BooleanField(default=True) # can login 
	staff        = models.BooleanField(default=False) # staff user non superuser
	admin        = models.BooleanField(default=False) # superuser 
	timestamp    = models.DateTimeField(auto_now_add=True)
	expire       = models.DateTimeField(null=True, blank=True)
	# confirm     = models.BooleanField(default=False)
	# confirmed_date     = models.DateTimeField(default=False)

	USERNAME_FIELD = 'phone_number' #username
	# USERNAME_FIELD and password are required by default
	REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

	objects = UserManager()

	def __unicode__(self):
		return "{} - {}".format(self.phone_number, self.full_name)

	def get_full_name(self):
		if self.full_name:
			return self.full_name
		return self.phone_number

	def get_short_name(self):
		return self.phone_number

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

class Profile(models.Model):
	choices = (
		(0, 'کاربر عادی'),
		(1, 'مغازه'),
	)
	user						= models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	user_type				= models.IntegerField(choices=choices, default=0)
	card_number			= models.CharField(max_length=11, null=True, blank=True)
	address					= models.CharField(max_length=255, null=True, blank=True)

	def __unicode__(self):
		return "{}".format(self.user)

# @receiver(post_save, sender=User)
# def build_profile_on_user_creation(sender, instance, created, **kwargs):
# 	if created:
# 		profile = Profile(user=instance)
# 		profile.save()

def create_random_password():
	pl = random.sample([1,2,3,4,5,6,7,8,9,0],4)
	passcode = ''.join(str(p) for p in pl)
	return passcode