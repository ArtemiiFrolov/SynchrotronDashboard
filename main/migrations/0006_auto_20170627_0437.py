# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_applicationcounter_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='end',
            field=models.DateTimeField(verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='application',
            name='start',
            field=models.DateTimeField(verbose_name='Старт'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Старт'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='end',
            field=models.DateTimeField(verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='start',
            field=models.DateTimeField(verbose_name='Старт'),
        ),
        migrations.AlterField(
            model_name='experimentplan',
            name='end',
            field=models.DateTimeField(verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='experimentplan',
            name='start',
            field=models.DateTimeField(verbose_name='Старт'),
        ),
    ]