# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-17 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_stagestatus_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagestatus',
            name='color',
            field=models.CharField(choices=[('#33СС01', 'Зеленый'), ('#FF0000', 'Красный'), ('#FFFFA0', 'Желтый')], default='#33СС00', max_length=7, verbose_name='Цвет'),
        ),
    ]
