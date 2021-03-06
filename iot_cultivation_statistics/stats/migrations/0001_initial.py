# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 16:58
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name=b'measurement date')),
                ('temperature', models.FloatField(blank=True, null=True, verbose_name=b'temperature')),
                ('airHumidity', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name=b'air humidity')),
                ('soilHumidity', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name=b'soil humidity')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150)),
                ('uuid', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name=b'watering date')),
                ('amount', models.IntegerField(verbose_name=b'amount in milliliters')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Plant')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Plant'),
        ),
    ]
