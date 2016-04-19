from chartjs.colors import COLORS, next_color
from chartjs.views.lines import BaseLineChartView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView

from iot_cultivation_statistics.stats.forms import PlantForm, PlantDetailForm
from iot_cultivation_statistics.stats.models import Plant, Measurement
from iot_cultivation_statistics.stats.models import PlantSettings


class PlantList(ListView, LoginRequiredMixin):
    model = Plant
    template_name = 'plant_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        qs = super(PlantList, self).get_queryset()
        return qs.filter(user=self.request.user)


class NewPlantFormView(CreateView, LoginRequiredMixin):
    form_class = PlantForm
    template_name = 'plant_form.html'
    success_url = reverse_lazy('stats:plants_list')

    def form_valid(self, form):
        return super(NewPlantFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewPlantFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PlantDetailView(DetailView):
    model = Plant
    template_name = 'plant_details.html'
    context_object_name = 'plant'

    def get_context_data(self, **kwargs):
        ctx = super(PlantDetailView, self).get_context_data(**kwargs)
        ctx['measurments'] = Measurement.objects.filter(plant=self.object)
        return ctx


class PlantSettingsView(UpdateView):
    model = PlantSettings
    template_name = 'plant_settings.html'
    fields = ['mode', 'value']

    def get_object(self, queryset=None):
        plant_slug = self.kwargs.get('slug', '')
        plant = Plant.objects.get(slug=plant_slug)
        PlantSettings.objects.get_or_create(plant=plant)
        return plant.plantsettings

    def get_success_url(self):
        plant_slug = self.kwargs.get('slug', '')
        plant = Plant.objects.get(slug=plant_slug)
        return plant.get_absolute_url()


class NewMeasurementFormView(CreateView, LoginRequiredMixin):
    form_class = PlantDetailForm
    template_name = 'plant_details_form.html'

    def get_success_url(self):
        plant_slug = self.kwargs.get('slug', '')
        return reverse('stats:plant_details', args=(plant_slug,))

    def form_valid(self, form):
        return super(NewMeasurementFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewMeasurementFormView, self).get_form_kwargs()
        plant_slug = self.kwargs.get('slug', '')
        plant = Plant.objects.get(slug=plant_slug)
        kwargs['plant'] = plant
        return kwargs


class NewMeasurementAPIFormView(CreateView):
    form_class = PlantDetailForm
    template_name = 'plant_details_form.html'

    def get_form_kwargs(self):
        kwargs = super(NewMeasurementAPIFormView, self).get_form_kwargs()
        plant_uuid = self.kwargs.get('uuid', '')
        plant = Plant.objects.get(uuid=plant_uuid)
        kwargs['plant'] = plant
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'water': '200'})

    def form_invalid(self, form):
        return HttpResponse(status=400)


class ChartDataView(BaseLineChartView):
    def get_plant(self):
        slug = self.kwargs.get('slug', '')
        return Plant.objects.get(slug=slug)

    def get_measurements(self):
        return Measurement.objects.filter(plant=self.get_plant()).order_by('date')

    def get_labels(self):
        measurements = self.get_measurements()
        measurements = measurements.values('date')
        measurements = map(lambda x: x['date'].strftime("%x %H:%M"), measurements)
        return measurements

    def get_data(self):
        """Return 3 datasets to plot."""

        measurements = self.get_measurements()
        measurements = measurements.values('temperature', 'soil_humidity', 'air_humidity')
        measurements = [
            map(lambda x: x['temperature'], measurements),
            map(lambda x: x['soil_humidity'], measurements),
            map(lambda x: x['air_humidity'], measurements),
        ]
        return measurements

    def get_context_data(self, *agrs, **kwargs):
        data = {}
        data['labels'] = self.get_labels()
        data['datasets'] = self.get_datasets()
        data['colors'] = self.get_colors()
        return data

    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        return next_color([
            (200, 200, 0),
            (128, 42, 42),
            (0, 0, 200),
        ])
