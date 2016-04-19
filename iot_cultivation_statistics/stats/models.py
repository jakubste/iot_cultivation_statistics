# coding=utf-8
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Plant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    uuid = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            slug = slugify(self.name)
            original_slug = slug
            while Plant.objects.filter(slug=slug):
                slug = original_slug + str(uuid4())[:3]

            self.slug = slug
            self.uuid = str(uuid4())[-12:]
        return super(Plant, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stats:plant_details', args=(self.slug,))


class Measurement(models.Model):
    plant = models.ForeignKey(Plant)
    date = models.DateTimeField('measurement date')
    temperature = models.FloatField('temperature', null=True, blank=True)
    air_humidity = models.FloatField(
        'air humidity',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    soil_humidity = models.FloatField(
        'soil humidity',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )


class Watering(models.Model):
    plant = models.ForeignKey(Plant)
    date = models.DateTimeField('watering date')
    amount = models.IntegerField('amount in milliliters')


class PlantSettings(models.Model):
    TIME_BASED = 't'
    HUMIDITY_BASED = 'h'
    DEACTIVATE = 'd'

    MODE_CHOICES = (
        (TIME_BASED, 'Czasowo'),
        (HUMIDITY_BASED, 'Na podstawie wilgotności'),
        (DEACTIVATE, 'Wyłącz'),
    )

    plant = models.OneToOneField(Plant)
    mode = models.CharField(choices=MODE_CHOICES, max_length=1, default=DEACTIVATE)
    value = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)]
    )
