from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Plant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    uuid = models.CharField(max_length=30)


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
