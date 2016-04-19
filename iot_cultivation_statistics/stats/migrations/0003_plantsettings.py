# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20160417_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mode', models.CharField(default=b'd', max_length=1, choices=[(b't', b'Czasowo'), (b'h', b'Na podstawie wilgotno\xc5\x9bci'), (b'd', b'Wy\xc5\x82\xc4\x85cz')])),
                ('value', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('plant', models.OneToOneField(to='stats.Plant')),
            ],
        ),
    ]
