from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
  url(r'^confirm/$', views.confirmation, name='confirmation'),
  url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
  url(r'^name/$', views.get_full_name, name='get_full_name'),
  #url(r'^register/$', views.register, name='register'),
]