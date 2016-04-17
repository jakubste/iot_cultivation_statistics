# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirHumidity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.IntegerField()),
                ('date', models.DateTimeField(verbose_name='measurement date')),
                ('humidity', models.FloatField(verbose_name='air humidity')),
            ],
        ),
        migrations.CreateModel(
            name='SoilHumidity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.IntegerField()),
                ('date', models.DateTimeField(verbose_name='measurement date')),
                ('humidity', models.FloatField(verbose_name='soil humidity')),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.IntegerField()),
                ('date', models.DateTimeField(verbose_name='measurement date')),
                ('temp', models.FloatField(verbose_name='temperature')),
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.IntegerField()),
                ('date', models.DateTimeField(verbose_name='watering date')),
                ('amount', models.FloatField(verbose_name='amount in liters')),
            ],
        ),
    ]
