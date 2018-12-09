from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main_page, name='main_page'),
	url(r'^transaction_confirmation/$', views.transaction_confirmation, name='transaction_confirmation'),
	url(r'^transaction/$', views.transaction, name='transaction'),
	url(r'^transaction/response/$', views.transaction_response, name='transaction_response'),
	url(r'^checkout/$', views.checkout, name='checkout'),
	url(r'^card_info/$', views.get_card_num_page, name='get_card_num_page'),
]
