# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.utils import timezone

from .forms import LoginForm, ConfirmationForm, GetFullNameForm
from .models import Profile
from accounts.models import User

from kavenegar import *

def send_sms(receiver, msg):
	try:
		api = KavenegarAPI('6E51437372544F62764A794E766A484C727A686B44387A31736352392B542F70')
		params = {
			# 'sender': '200004346',#optional
			'receptor': receiver,#multiple mobile number, split by comma
			'message': msg,
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e: 
		print(e)
	except HTTPException as e: 
		print(e)

def login(request):
	if request.user.is_authenticated():
		return redirect('main_page')
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			user, password = User.objects.new_or_get(phone_number)
			request.session['phone_number'] = phone_number
			msg = 'استلا\nکد تایید: {}'.format(password)
			send_sms(phone_number, msg)
			################################################################################################# send sms here
			print password, phone_number
			try:
				next_url = request.GET['next_url']
				response = redirect('confirmation')
				response['Location'] += '?next_url=' + next_url
				return response
			except:
				return redirect('confirmation')
	return render(request, 'accounts/login.html', {'form': form})

def confirmation(request):
	if request.user.is_authenticated():
		return redirect('main_page')
	try:
		phone_number = request.session['phone_number']
	except:
		return redirect('login')
	form = ConfirmationForm()
	if request.method == 'POST':
		form = ConfirmationForm(request.POST)
		if form.is_valid():
			activation_code = form.cleaned_data['activation_code']
			user = authenticate(phone_number=phone_number, password=activation_code)
			if not user:
				err_msg = 'کد وارد شده صحیح نمی‌باشد'
				messages.add_message(request, messages.ERROR, err_msg)
				return redirect('confirmation')
			if user.expire < timezone.now():
				err_msg = 'کد وارد شده منقضی شده است، لطفا دوباره شماره تماس خود را وارد نمایید'
				messages.add_message(request, messages.ERROR, err_msg)
				return redirect('login')
			auth.login(request, user)
			try:
				next_url = request.GET['next_url']
			except:
				next_url = "/"
			if not user.full_name or user.full_name == '':
				response = redirect('get_full_name')
				if next_url != '/':
					response['Location'] += '?nex_url=' + next_url
				return response
			return redirect(next_url)
	return render(request, 'accounts/confirm.html', {'form': form})

def get_full_name(request):
	user = request.user
	if not user.is_authenticated():
		return redirect('login')
	form = GetFullNameForm(instance=user)
	if request.method == 'POST':
		form = GetFullNameForm(request.POST)
		if form.is_valid():
			full_name = form.cleaned_data['full_name']
			user.full_name = full_name
			user.save()
			try:
				next_url = request.GET['next_url']
			except:
				next_url = "/"
			return redirect(next_url)
	return render(request, 'accounts/get_full_name.html', {'form': form})