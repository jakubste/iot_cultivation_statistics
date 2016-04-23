# coding=utf-8
from datetime import datetime
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Plant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField('nazwa', max_length=150)
    slug = models.SlugField(max_length=150)
    uuid = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            slug = slugify(self.name)
            original_slug = slug
            # uniqe
            while Plant.objects.filter(slug=slug):
                slug = original_slug + str(uuid4())[:3]

            self.slug = slug
            self.uuid = str(uuid4())[-12:]
        return super(Plant, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stats:plant_details', args=(self.slug,))


class Measurement(models.Model):
    plant = models.ForeignKey(Plant, related_name='measurements')
    date = models.DateTimeField('data pomiaru')
    temperature = models.FloatField('temperatura')
    air_humidity = models.FloatField(
        'wilgotność powietrza',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    soil_humidity = models.FloatField(
        'wilgotność gleby',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )


class Watering(models.Model):
    plant = models.ForeignKey(Plant, related_name='waterings')
    date = models.DateTimeField('data podlania', default=datetime.now)
    amount = models.IntegerField('ilość w mililitrach')


class PlantSettings(models.Model):
    TIME_BASED = 't'
    HUMIDITY_BASED = 'h'
    DEACTIVATE = 'd'

    MODE_CHOICES = (
        (TIME_BASED, 'Co określony czas'),
        (HUMIDITY_BASED, 'Na podstawie wilgotności'),
        (DEACTIVATE, 'Dezaktywuj automatyczne podlewanie'),
    )

    plant = models.OneToOneField(Plant)
    mode = models.CharField('tryb', choices=MODE_CHOICES, max_length=1, default=DEACTIVATE)
    value = models.FloatField(
        'wartość',
        default=0,
        validators=[MinValueValidator(0)]
    )
    amount = models.IntegerField(
        'ilość',
        default=0
    )
