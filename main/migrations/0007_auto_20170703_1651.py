# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170627_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='serial',
            field=models.CharField(max_length=15, unique=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='eventslist',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='journalstatus',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='right',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Название'),
        ),
    ]
