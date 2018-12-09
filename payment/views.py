# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from pay_ir.api.client import PayIrClient
from pay_ir.utils.reqres import get_json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Q

from accounts.models import User
from .forms import TransactionForm, CardNumForm
from .models import Transaction, Deposit, Checkout
from shops.models import Shop, Discount, OwnerPhoneNumber
from accounts.views import send_sms
from shops.models import OwnerPhoneNumber

# API_KEY = 'test'
# RETURN_URL = 'http://localhost:8000/payments/transaction/response/'

API_KEY = '90a9cff2b9a5e698d629fd8865c516b9'
RETURN_URL = 'http://stellaclub.ir/payments/transaction/response/'

def main_page(request):
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			amount = int(form.cleaned_data['amount'])
			receiver = form.cleaned_data['receiver']
			try:
				receiver_user = User.objects.get(Q(username=receiver) | Q(phone_number=receiver))
			except User.DoesNotExist:
				messages.add_message(
					request, 
					messages.ERROR, 
					'نام کاربری - شماره تماس گیرنده اشتباه است!'
				)
				context = {
					'form': TransactionForm(),
				}
				return render(request, 'payment/index.html', context)
			request.session['receiver'] = receiver
			request.session['amount'] = amount
			if request.user.is_authenticated:
				return redirect('transaction_confirmation')
			else:
				next_url = reverse('transaction_confirmation')
				response = redirect('login')
				response['Location'] += '?next_url=' + next_url
				return response
	else:
		form = TransactionForm()
	context = {
		'form': form,
		'discounts': Discount.objects.all(),
	}
	return render(request, 'payment/index.html', context)

def transaction_confirmation(request):
	amount = request.session['amount']
	receiver = request.session['receiver']
	try:
		receiver_user = Shop.objects.get(pk=receiver)
	except User.DoesNotExist:
		messages.add_message(
			request, 
			messages.ERROR, 
			'نام کاربری-شماره تماس گیرنده اشتباه است!'
		)
		context = {
			'form': TransactionForm(),
		}
		return render(request, 'payment/index.html', context)
	try:
		discount = Discount.objects.get(
			shop=receiver_user, 
			is_expire=False,
			expiration_date__gte=timezone.now(),
		)
		discount_amount = (amount * discount.percentage)/(100)
		discount_message = 'با پرداخت {} تومان، قلک شما {} تومان شارژ می‌شود.'.format(amount, discount_amount)
	except Discount.DoesNotExist:
		discount = False
		discount_message = ''
	context = {
		'receiver_user': receiver_user,
		'amount': amount,
		'discount_message': discount_message,
	}
	return render(request, 'payment/transaction_confirmation.html', context)

def transaction(request):
	if not request.user.is_authenticated:
		return redirect('login')

	amount = request.session['amount']
	if not amount:
		return redirect('main_page')

	client = PayIrClient(API_KEY)
	redirect_url = str(RETURN_URL)
	response = client.init_transaction(int(amount) * 10, redirect_url)
	trans_id = int(response['trans_id'])
	return HttpResponseRedirect(response['payment_url'])

@csrf_exempt
def transaction_response(request):
	transaction = False
	deposit = False
	discount_amount = 0
	if not request.user.is_authenticated:
		return redirect('login')
	
	receiver = request.session['receiver']
	amount = request.session['amount']

	try:
		deposit = Deposit.objects.get(user=request.user)
	except Deposit.DoesNotExist:
		deposit = Deposit.objects.create(user=request.user)

	try:
		receiver_user = Shop.objects.get(pk=receiver)
	except User.DoesNotExist:
		return HttpResponse('نام کاربری گیرنده اشتباه است!')
	transaction = Transaction.objects.create(
		transaction_id=request.POST['transId'],
		shop=receiver_user,
		user=request.user,
		amount=int(amount),
	)

	if request.method == "POST":
		if request.POST['status'] != '0':
			try:
				verify_data = {
					'api': API_KEY,
					'transId': int(request.POST['transId'])
				}
				if Transaction.objects.filter(is_successful=True, transaction_id=request.POST['transId']).exists():
					return HttpResponse('1 خطا')
				response = get_json(requests.post('https://pay.ir/payment/verify', data=verify_data))
				if response['status'] == 1:
					############### NOTIFY SHOP OWNER
					try:
						shop_owner_number = OwnerPhoneNumber.objects.get(shop=receiver_user).num
						send_sms(
							shop_owner_number, 
							'مبلغ {} توسط {} پرداخت شد. این مبلغ تا ۲۴ ساعت آینده به حساب شما واریز می‌شود.'.format(amount, request.user.full_name)
						)
					except OwnerPhoneNumber.DoesNotExist:
						pass
					transaction.is_successful = True
					transaction.save()
					try:
						discount = Discount.objects.get(
							shop=receiver_user, 
							is_expire=False,
							start_date__lte=timezone.now(),
							expiration_date__gte=timezone.now(),
						)
						discount_amount = (amount * discount.percentage)/(100)
						deposit.total += discount_amount
						deposit.save()
					except Discount.DoesNotExist:
						pass
				else:
					return HttpResponse('2 خطا')
			except IntegrityError as e: 
				return HttpResponse('3 خطا' + e.message)
	context = {
		'transaction': transaction,
		'deposit': deposit,
		'discount_amount': discount_amount,
	}
	return render(request, 'payment/transaction_result.html', context)

def get_card_num_page(request):
	if not request.user.is_authenticated:
		next_url = reverse('checkout')
		response = redirect('login')
		response['Location'] += '?next_url=' + next_url
		return response
	if request.method == 'POST':
		form = CardNumForm(instance=request.user, data=request.POST)
		if form.is_valid():
			print "YES"
			form.save()
			next_url = request.GET.get('next_url')
			if next_url:
				return redirect(next_url)
			else:
				return redirect('checkout')
		else:
			print "NO"
	context = {
		'form': CardNumForm(instance=request.user)
	}
	return render(request, 'payment/card_num.html', context)


def checkout(request):
	if not request.user.is_authenticated:
		next_url = reverse('checkout')
		response = redirect('login')
		response['Location'] += '?next_url=' + next_url
		return response
	if not request.user.card_num or request.user.card_num == '':
		next_url = reverse('checkout')
		response = redirect('get_card_num_page')
		response['Location'] += '?next_url=' + next_url
		return response
	try:
		deposit = Deposit.objects.get(user=request.user)
	except Deposit.DoesNotExist:
		deposit = None
	if request.method == "POST":
		checkout = Checkout.objects.create(
			user=request.user,
			amount=deposit.total
		)
		deposit.total = 0
		deposit.save()
		messages.add_message(
			request, 
			messages.SUCCESS, 
			'درخواست تسویه حساب شما با موفقیت ارسال شد و تا ۴۸ ساعت آینده به حساب شما واریز می‌شود.'
		)
	checkouts = Checkout.objects.filter(user=request.user)
	context = {
		'deposit': deposit,
		'checkouts': checkouts,
	}
	return render(request, 'payment/checkout.html', context)