# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentplan',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planning_experiments', to='main.Station', verbose_name='Станция'),
        ),
    ]
