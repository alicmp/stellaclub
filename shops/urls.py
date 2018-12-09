from django.conf.urls import url, include
from .views import explore_result, shop_page, special_offer_page

urlpatterns = [
  url(r'^explore/$', explore_result, name='explore_result'),
  url(r'^special/$', special_offer_page, name='special_offer_page'),
  url(r'^shop/(?P<shop_id>[0-9]+)$', shop_page, name='shop_page'),
]
