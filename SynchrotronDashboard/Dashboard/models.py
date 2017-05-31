from django.db import models
from datetime import datetime
#добавить календари и документы!!!
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
	
class CompleteStatus (models.Model):
    name=models.CharField(max_length=100)

class StageStatus(models.Model):
    name=models.CharField(max_length=100)
	
class JournalStatus(models.Model):
    name=models.CharField(max_length=100)
	
class EventsList(models.Model):
    name=models.CharField(max_length=100)

class Request(models.Model):
    #добавить файл с договором, файл с отчетом, статью
    name=models.CharField(max_length=200)
    author=models.ForeignKey(User, related_name='requests_as_author')
    organizations=models.ManyToManyField(Organization, related_name='requests')
    serial=models.CharField(max_length=15)
    description=models.CharField(max_length=2000)
    time_needed=models.IntegerField(default=0)
    time_start=models.DateTimeField(auto_now_add=True)
    time_end=models.DateTimeField(auto_now_add=True)
    station=models.ForeignKey(Station, related_name='requests')
    metodic=models.ManyToManyField(Metodic, related_name='requests')
    participant=models.ManyToManyField(User, related_name='requests_as_participant')
    equipment=models.ManyToManyField(Equipment, related_name='requests')
    complete_status=models.ForeignKey(CompleteStatus,related_name='requests')
    stage_status=models.ForeignKey(StageStatus,related_name='requests')	

class PlaningExperiment (models.Model):
    author=models.ForeignKey(User)
    request=models.ForeignKey(Request,related_name='planning_experiments')
    time_start=models.DateTimeField(auto_now_add=True)
    time_end=models.DateTimeField(auto_now_add=True)
    status=models.ForeignKey(JournalStatus,related_name='planning_experiments')	
	
class Experiment(models.Model):
    request=models.ForeignKey(Request,related_name='experiments')
    auhtor=models.ForeignKey(User) #добавить автоматическое заполнение из request
    time_start=models.DateTimeField(auto_now_add=True)
    time_end=models.DateTimeField(auto_now_add=True)
    operator=models.ForeignKey(User, related_name='experiments')
    metodic=models.ForeignKey(Metodic, related_name='experiments')
	
class Event(models.Model):
    name=models.ForeignKey(EventsList)
    time_start=models.DateTimeField(auto_now_add=True)
    time_end=models.DateTimeField(auto_now_add=True)
	
class Comment(models.Model):
    request=models.ForeignKey(Request)
    author=models.ForeignKey(User)
    time_written=models.DateTimeField(auto_now_add=True)
    text=models.CharField(max_length=1000)
    request=models.ForeignKey(Request)