# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Shop, Discount
from payment.forms import TransactionForm

def get_choice_key(value):
	choices = (
		(0, 'کافی_شاپ'),
		(1, 'سرگرمی'),
		(2, 'رستوران')
	)
	for c in choices:
		if c[1] == value:
			return c[0]

def explore_result(request):
	category = request.GET.get('cat')
	discounts = Discount.objects.filter(
		is_expire=False,
		expiration_date__gte=timezone.now(),
		shop__category=get_choice_key(category),
	)
	context = {
		'discounts': discounts,
	}
	return render(request, "shops/shop_list.html", context)

def special_offer_page(request):
	discounts = Discount.objects.filter(
		is_expire=False,
		expiration_date__gte=timezone.now()
	)
	context = {
		'title': 'پیشنهادهای ویژه شیراز',
		'discounts': discounts,
	}
	return render(request, "shops/shop_list.html", context)

def shop_page(request, shop_id):
	shop = get_object_or_404(Shop, pk=shop_id)
	try:
		discount = Discount.objects.get(shop=shop)
	except Discount.DoesNotExist:
		discount = None

	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			amount = int(form.cleaned_data['amount'])
			receiver = form.cleaned_data['receiver']
			try:
				receiver_user = Shop.objects.get(id=receiver)
			except User.DoesNotExist:
				messages.add_message(
					request, 
					messages.ERROR, 
					'نام کاربری - شماره تماس گیرنده اشتباه است!'
				)
				context = {
					'form': TransactionForm(initial={'receiver': shop.id}),
				}
				return render(request, 'shops/shop.html', context)
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
		form = TransactionForm(initial={'receiver': shop.id})
	context = {
		'shop': shop,
		'discount': discount,
		'form': form,
	}
	return render(request, "shops/shop.html", context)