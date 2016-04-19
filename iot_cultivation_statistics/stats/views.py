from datetime import datetime, timedelta

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
        plant = self.get_plant()
        kwargs['plant'] = plant
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return self.send_watering_info()

    def form_invalid(self, form):
        return HttpResponse(status=400)

    def send_watering_info(self):
        settings = self.get_plant().plantsettings
        if(settings.mode == PlantSettings.TIME_BASED):
            last_watering = self.get_plant().waterings.order_by('-date')
            if not last_watering or last_watering[0].date < datetime.now() - timedelta(hourd=settings.value):
                return JsonResponse({'water': settings.amount})
        elif (settings.mode == PlantSettings.HUMIDITY_BASED):
            humidity = self.get_plant().measurements.order_by('-date')
            if not humidity or humidity[0].soil_humidity < settings.value:
                return JsonResponse({'water': settings.amount})
        return HttpResponse(status=201)

    def get_plant(self):
        plant_uuid = self.kwargs.get('uuid', '')
        return Plant.objects.get(uuid=plant_uuid)
