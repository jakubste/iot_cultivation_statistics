from django.conf.urls import url

from iot_cultivation_statistics.stats.views import *

urlpatterns = [
    url(r'^twoje_rosliny/$', PlantList.as_view(), name='plants_list'),
    url(r'^dodaj_rosline/$', NewPlantFormView.as_view(), name='new_plant'),
    url(r'^statystyki/(?P<slug>\w+)/$', PlantDetailView.as_view(), name='plant_details'),
    url(r'^ustawienia/(?P<slug>\w+)/$', PlantSettingsView.as_view(), name='plant_settings'),
    url(r'^dodaj_pomiar/(?P<slug>\w+)/$', NewMeasurementFormView.as_view(), name='new_measurement'),
    url(r'^dodaj_pomiar_api/(?P<uuid>\w+)/$', NewMeasurementAPIFormView.as_view(), name='new_measurement_API'),
    url(r'^chart/(?P<slug>\w+)/$', ChartDataView.as_view(), name='chart'),
]
