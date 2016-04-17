from django.conf.urls import url

from iot_cultivation_statistics.stats.views import *

urlpatterns = [
    url(r'^$', Stats.as_view(), name='stats'),
]
