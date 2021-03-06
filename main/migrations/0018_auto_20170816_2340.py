# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20170814_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'permissions': (('view_application', 'Может смотреть заявку'), ('view_all_applications', 'Может смотреть все заявки'), ('edit_applications', 'Может редактировать заявки'), ('approve_applications', 'Может принимать заявки'), ('decline_applications', 'Может отклонять заявки'), ('return_applications', 'Может возвращать заявки')), 'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': (('add_event_to_calendar', 'Может добавлять события в календарь'),), 'verbose_name': 'Событие', 'verbose_name_plural': 'События'},
        ),
        migrations.AlterModelOptions(
            name='experiment',
            options={'permissions': (('conduct_station_experiment', 'Может проводить эксперимент'), ('view_station_experiment', 'Может просматривать эксперимент')), 'verbose_name': 'Завершенный эксперимент', 'verbose_name_plural': 'Завершенные эксперименты'},
        ),
        migrations.AlterModelOptions(
            name='experimentplan',
            options={'permissions': (('view_plan_station_experiment', 'Может просматривать запланированный эксперимент'), ('plan_station_experiment', 'Может планировать эксперимент')), 'verbose_name': 'Планируемый эксперимент', 'verbose_name_plural': 'Планируемые эксперименты'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'permissions': (('view_station_application', 'Может смотреть заявки станции'), ('edit_station_application', 'Может редактировать заявки станции'), ('approve_station_application', 'Может принимать заявки станции'), ('view_plan_station_experiment', 'Может просматривать запланированный эксперимент на станции'), ('plan_station_experiment', 'Может планировать эксперимент на станции'), ('conduct_station_experiment', 'Может проводить эксперимент на станции'), ('view_station_experiment', 'Может просматривать эксперимент на станции')), 'verbose_name': 'Станция', 'verbose_name_plural': 'Станции'},
        ),
    ]
