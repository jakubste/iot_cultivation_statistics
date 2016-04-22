from django.conf.urls import url

from iot_cultivation_statistics.accounts.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^zaloguj/$', LoginView.as_view(), name='login'),
    url(r'^wyloguj/$', logout_view, name='logout'),
    url(r'^zarejestruj/$', RegisterView.as_view(), name='register'),
]