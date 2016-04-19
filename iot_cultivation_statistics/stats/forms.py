import uuid
from datetime import datetime

from django.forms import ModelForm
from django.utils.text import slugify

from iot_cultivation_statistics.stats.models import Plant, Measurement


class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PlantForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        plant = super(PlantForm, self).save(False)
        if commit:
            plant.user = self.user
            plant.save()
        return plant

class PlantDetailForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'temperature', 'air_humidity', 'soil_humidity']

    def __init__(self, *args, **kwargs):
        self.plant = kwargs.pop('plant')
        super(PlantDetailForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.now()

    def save(self, commit=True):
        plantDetails = super(PlantDetailForm, self).save(False)
        if commit:
            plantDetails.plant = self.plant
            plantDetails.save()
        return plantDetails