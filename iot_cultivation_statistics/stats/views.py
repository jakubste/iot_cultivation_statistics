from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.debug import sensitive_variables
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class Stats(TemplateView):
    template_name = 'stats.html'
