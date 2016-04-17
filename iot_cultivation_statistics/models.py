from django.db import models

class Plants(models.Model):
	userId = models.IntegerField()
	plantId = models.IntegerField()

class Measurement(models.Model):
    plant = models.ForeignKey(Plants)
    date = models.DateTimeField('measurement date')
    temp = models.FloatField('temperature')
    airHumidity = models.FloatField('air humidity')
    soilHumidity = models.FloatField('soil humidity')

class Watering(models.Model):
    plant = models.ForeignKey(Plants)
    date = models.DateTimeField('watering date')
    amount = models.FloatField('amount in liters')