# -*- coding: utf-8 -*-

import django

django.setup()

from main.models import *


organization1 = Organization.objects.create(name='ЛМА')
organization2 = Organization.objects.create(name='Курчатовский НИИ')

station1 = Station.objects.create(name='Белок', short_description='БЕЛ')
station2 = Station.objects.create(name='Кристалл', short_description='КРИ')

approach1 = Approach.objects.create(name='Бомбардировка', description='Бомбардировка нейтронами')
approach2 = Approach.objects.create(name='Отражени', description='Измерение угла отражения')

right1 = Right.objects.create(name='Создать юзера')
right2 = Right.objects.create(name='Пользование сайтом')

role1 = Role.objects.create(name='Член комиссии')
role1.rights.add(right1, right2)
role2 = Role.objects.create(name='Пользователь')
role2.rights.add(right2)

equipment1 = Equipment.objects.create(name='Особое оборудование')
equipment2 = Equipment.objects.create(name='Важное оборудование')

completeStatus1 = CompleteStatus.objects.create(name='Отчет не отправлен')
completeStatus2 = CompleteStatus.objects.create(name='Отчет возвращен с поправками')

stageStatus1 = StageStatus.objects.create(name='Заявка не подтверждена')
stageStatus2 = StageStatus.objects.create(name='Заявка подтверждена')

journalStatus1 = JournalStatus.objects.create(name='Эксперимент назначен')
journalStatus2 = JournalStatus.objects.create(name='Эксперимент не назначен')

eventsList1 = EventsList.objects.create(name='Запланированная работа')
eventsList2 = EventsList.objects.create(name='Профилактика')

user1 = User.objects.create(email='123@gmail.com', name='Васильев В.А.', role=role1)
user1.station.add(station1, station2)
user1.organization.add(organization1)
user1.special_rights.add(right1)
user2 = User.objects.create(email='petrov@gmail.com', name='Петров А.З.', role=role2)
user2.station.add(station1)
user2.organization.add(organization1, organization2)
user2.special_rights.add(right1)

#application1 = Application.objects.create(name='Изучение образца в янтаре', author=user1,organizatio)
