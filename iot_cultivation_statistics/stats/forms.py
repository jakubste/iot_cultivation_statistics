from datetime import datetime

from django.forms import ModelForm

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


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'temperature', 'air_humidity', 'soil_humidity', 'insolation']

    def __init__(self, *args, **kwargs):
        self.plant = kwargs.pop('plant')
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = False
        self.fields['date'].initial = datetime.now()

    def clean_date(self):
        date = self.cleaned_data.get('date', None)
        if not date:
            date = datetime.now()
        return date

    def save(self, commit=True):
        measurement = super(MeasurementForm, self).save(False)
        if commit:
            measurement.plant = self.plant
            measurement.save()
        return measurement
