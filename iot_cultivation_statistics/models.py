from django.db import models

class Temperature(models.Model):
    deviceId = models.IntegerField()
    date = models.DateTimeField('measurement date')
    temp = models.FloatField('temperature')

class AirHumidity(models.Model):
    deviceId = models.IntegerField()
    date = models.DateTimeField('measurement date')
    humidity = models.FloatField('air humidity')

class SoilHumidity(models.Model):
    deviceId = models.IntegerField()
    date = models.DateTimeField('measurement date')
    humidity = models.FloatField('soil humidity')

class Watering(models.Model):
    deviceId = models.IntegerField()
    date = models.DateTimeField('watering date')
    amount = models.FloatField('amount in liters')