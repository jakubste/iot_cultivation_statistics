from django.views.generic.list import ListView


class PlantList(ListView):
    template_name = 'plant_list.html'
