# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-22 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20170822_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='special_group_permissions',
            field=models.ManyToManyField(blank=True, to='main.SpecialGroupPermission', verbose_name='Особые права групп'),
        ),
        migrations.AddField(
            model_name='station',
            name='special_user_permissions',
            field=models.ManyToManyField(blank=True, to='main.SpecialUserPermission', verbose_name='Особые права пользователей'),
        ),
    ]
