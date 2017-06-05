from django.db import models
from datetime import datetime
#добавить календари и документы!!!
class Organization(models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name

class Station(models.Model):
    name=models.CharField(max_length=100,default="")
    short_description=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
    @property
    def ahref_name(self):
        return '<a href="/stations/' +self.short_description+' ">'+self.name+'</a>'

class Metodic(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=1000,default="")
    def __str__(self):
        return self.name

class Right(models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name

class Role(models.Model):
    name=models.CharField(max_length=100,default="")
    rights=models.ManyToManyField(Right, related_name='roles')
    def __str__(self):
        return self.name

class User(models.Model):
    name=models.CharField(max_length=100,default="")
    station=models.ManyToManyField(Station,related_name='users')
    organization=models.ManyToManyField(Organization,related_name='users')
    role=models.ForeignKey(Role,related_name='users')
    special_rights=models.ManyToManyField(Right, related_name='users')
    def __str__(self):
        return self.name
    @property
    def ahref_name(self):
        return '<a href="/users/' +str(self.id)+' ">'+self.name+'</a>'

class Equipment (models.Model):
    name=models.CharField(max_length=150,default="")
    def __str__(self):
        return self.name
	
class CompleteStatus (models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name

class StageStatus(models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
	
class JournalStatus(models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
	
class EventsList(models.Model):
    name=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name

class Request(models.Model):
    #добавить файл с договором, файл с отчетом, статью
    name=models.CharField(max_length=200,default="")
    author=models.ForeignKey(User, related_name='requests_as_author')
    organizations=models.ManyToManyField(Organization, related_name='requests')
    serial=models.CharField(max_length=15,default="")
    description=models.CharField(max_length=2000,default="")
    time_needed=models.IntegerField(default=0)
    date_start=models.DateField(default=datetime.today)
    date_end=models.DateField(default=datetime.today)
    time_start=models.TimeField(default=datetime.now)
    time_end=models.TimeField(default=datetime.now)
    station=models.ForeignKey(Station, related_name='requests')
    metodic=models.ManyToManyField(Metodic, related_name='requests')
    participant=models.ManyToManyField(User, related_name='requests_as_participant')
    equipment=models.ManyToManyField(Equipment, related_name='requests')
    complete_status=models.ForeignKey(CompleteStatus,related_name='requests')
    stage_status=models.ForeignKey(StageStatus,related_name='requests')	
    def __str__(self):
        return self.serial
    @property
    def ahref_serial(self):
        return '<a href="/requests/' +self.serial+' ">'+self.serial+'</a>'
    @property
    def ahref_name(self):
        return '<a href="/requests/' +self.serial+' ">'+self.name+'</a>'
		
class PlaningExperiment (models.Model):
    author=models.ForeignKey(User, related_name='planning_experiments')
    request=models.ForeignKey(Request,related_name='planning_experiments')
    date_start=models.DateField(default=datetime.today)
    date_end=models.DateField(default=datetime.today)
    time_start=models.TimeField(default=datetime.now)
    time_end=models.TimeField(default=datetime.now)
    status=models.ForeignKey(JournalStatus,related_name='planning_experiments')
    station=models.ForeignKey(Station, related_name='planning_experiments')
    def __str__(self):
        if self.date_start==self.date_end:
            return self.station.name+" "+self.time_start.strftime(" %H:%M:%S - ")+self.time_end.strftime("%H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) ")
        else:
            return self.station.name+" "+self.time_start.strftime(" %H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) - ")+self.time_end.strftime("%H:%M:%S ")+self.date_end.strftime("(%d-%m-%Y)")

class Experiment(models.Model):
    request=models.ForeignKey(Request,related_name='experiments')
    author=models.ForeignKey(User,related_name='experiments_as_author') #добавить автоматическое заполнение из request
    date_start=models.DateField(default=datetime.today)
    date_end=models.DateField(default=datetime.today)
    time_start=models.TimeField(default=datetime.now)
    time_end=models.TimeField(default=datetime.now)
    operator=models.ForeignKey(User, related_name='experiments_as_operator')
    metodic=models.ForeignKey(Metodic, related_name='experiments')
    comment=models.CharField(max_length=200,default="")
    station=models.ForeignKey(Station, related_name='experiments')
    def __str__(self):
        if self.date_start==self.date_end:
            return self.station.name+" "+self.time_start.strftime(" %H:%M:%S - ")+self.time_end.strftime("%H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) ")
        else:
            return self.station.name+" "+self.time_start.strftime(" %H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) - ")+self.time_end.strftime("%H:%M:%S ")+self.date_end.strftime("(%d-%m-%Y)")

	
class Event(models.Model):
    name=models.ForeignKey(EventsList, related_name='events')
    date_start=models.DateField(default=datetime.today)
    date_end=models.DateField(default=datetime.today)
    time_start=models.TimeField(default=datetime.now)
    time_end=models.TimeField(default=datetime.now)
    def __str__(self):
        if self.date_start==self.date_end:
            return self.time_start.strftime(" %H:%M:%S - ")+self.time_end.strftime("%H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) ")
        else:
            return self.time_start.strftime(" %H:%M:%S ")+self.date_start.strftime("(%d-%m-%Y) - ")+self.time_end.strftime("%H:%M:%S ")+self.date_end.strftime("(%d-%m-%Y)")

	
class Comment(models.Model):
    request=models.ForeignKey(Request, related_name='comments')
    author=models.ForeignKey(User, related_name='comments')
    date_written=models.DateField(default=datetime.today)
    time_written=models.TimeField(default=datetime.today)
    text=models.CharField(max_length=1000,default="")
    def __str__(self):
        return self.author.name+" "+ self.request.serial+self.time_written.strftime(" %H:%M:%S - ")   