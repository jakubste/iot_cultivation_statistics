import uuid

from django.forms import ModelForm
from django.utils.text import slugify

from iot_cultivation_statistics.stats.models import Plant


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