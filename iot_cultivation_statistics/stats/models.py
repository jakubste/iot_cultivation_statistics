from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Plant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    uuid = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        original_slug = slug
        while Plant.objects.filter(slug=slug):
            slug = original_slug + str(uuid4())[:3]

        self.slug = slug
        self.uuid = str(uuid4())[-12:]
        return super(Plant, self).save(*args, **kwargs)


class Measurement(models.Model):
    plant = models.ForeignKey(Plant)
    date = models.DateTimeField('measurement date')
    temperature = models.FloatField('temperature', null=True, blank=True)
    airHumidity = models.FloatField(
        'air humidity',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    soilHumidity = models.FloatField(
        'soil humidity',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )


class Watering(models.Model):
    plant = models.ForeignKey(Plant)
    date = models.DateTimeField('watering date')
    amount = models.IntegerField('amount in milliliters')
