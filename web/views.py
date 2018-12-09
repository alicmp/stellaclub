# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
# from urllib.parse import quote

from django.shortcuts import render, HttpResponse, redirect
from django.utils.encoding import iri_to_uri
from django.utils import timezone

from shops.models import Discount, Shop
from payment.models import Transaction

def home_page(request):
  if request.method == 'POST':
    q = request.POST.get('txtSearch')
    response = redirect('search')
    response['Location'] += iri_to_uri('?term=%s' % q)
    return response
  
  discounts = Discount.objects.filter(
    is_expire=False, 
    expiration_date__gte=datetime.datetime.now()
  )
  context = {
    'discounts': discounts,
    'transactions': Transaction.objects.filter(is_successful=True)[:10]
  }
  return render(request, "web/index.html", context)

def autocomplete_search(request):
  if request.is_ajax():
    q = request.GET.get('term', '').capitalize()
    search_qs = Discount.objects.filter(
      is_expire=False,
      expiration_date__gte=timezone.now(),
      shop__name__contains=q
    )
    print search_qs
    results = []
    for r in search_qs:
      result_json = {}
      result_json['id'] = r.shop.id
      result_json['label'] = r.shop.name
      result_json['value'] = r.shop.name
      results.append(result_json)
    data = json.dumps(results)
  else:
    return 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def search(request):
  q = request.GET.get('term', '')
  search_qs = Discount.objects.filter(
    is_expire=False,
    expiration_date__gte=timezone.now(),
  )
  context = {
    'title': "نتایج جست و جوی شما برای %s" % q,
    'discounts': search_qs,
  }
  return render(request, "shops/shop_list.html", context)