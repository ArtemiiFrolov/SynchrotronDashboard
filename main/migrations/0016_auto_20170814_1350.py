# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-14 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_event_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='color',
            field=models.CharField(choices=[('#33СС00', 'Зеленый'), ('#0000FF', 'Синий'), ('#FF0000', 'Красный'), ('#33ССFF', 'Голубой'), ('#FF00FF', 'Розовый'), ('#660033', 'Коричневый'), ('#9900FF', 'Фиолетовый'), ('#СС0000', 'Темно-красный')], default='#33СС00', max_length=7, verbose_name='Цвет'),
        ),
    ]
