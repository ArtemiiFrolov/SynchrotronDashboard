from django.db import models
from datetime import datetime

class Organization(models.Model):
    name=models.CharField(max_length=100)

class Station(models.Model):
    name=models.CharField(max_length=100)

class Metodic(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)

class Rights(models.Model):
    name=models.CharField(max_length=100)

class Role(models.Model):
    name=models.CharField(max_length=100)
    rights=models.ManyToManyField(Rights)

class User(models.Model):
    name=models.CharField(max_length=100)
    station=models.ManyToManyField(Station)
    organization=models.ManyToManyField(Organization)
    role=models.ForeignKey(Role)
    special_rights=models.ManyToManyField(Rights)		

class Equipment (models.Model):
    name=models.CharField(max_length=150)

class Request(models.Model):
    #добавить файл с договором, файл с отчетом, статью
    name=models.CharField(max_length=200)
    organizations=models.ManyToManyField(Organization, related_name='requests')
    serial=models.CharField(max_length=15)
    description=models.CharField(max_length=2000)
    time_needed=models.IntegerField(default=0)
    time_start=models.TimeField(default=datetime.now)
    time_end=models.TimeField(default=datetime.now)
    station=models.ForeignKey(Station, related_name='requests')
    metodic=models.ManyToManyField(Metodic)
    participant=models.ManyToManyField(User)
    equipment=models.ManyToManyField(Equipment)
    status=models.CharField(max_length=100)			

class Comment(models.Model):
    request=models.ForeignKey(Request)
    author=models.ForeignKey(User)
    time_written=models.TimeField(default=datetime.now)
    text=models.CharField(max_length=1000)
    request=models.ForeignKey(Request)