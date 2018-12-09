from django.conf.urls import url, include
from .views import home_page, search, autocomplete_search

urlpatterns = [
  url(r'^$', home_page, name='home'),
  url(r'^search/', search, name='search'),
  url(r'^ajax_calls/search/', autocomplete_search, name='autocomplete_search'),
]
