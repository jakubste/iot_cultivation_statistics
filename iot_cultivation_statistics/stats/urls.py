from django.conf.urls import url

from iot_cultivation_statistics.stats.views import *

urlpatterns = [
    url(r'^twoje_rosliny/$', PlantList.as_view(), name='plants_list'),
    url(r'^dodaj_rosline/$', NewPlantFormView.as_view(), name='new_plant'),
]
