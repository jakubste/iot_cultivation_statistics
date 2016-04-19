from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from iot_cultivation_statistics.stats.forms import PlantForm
from iot_cultivation_statistics.stats.models import Plant, Measurement, PlantSettings


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
        print 'valid, lol'
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
