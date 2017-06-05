from django.contrib import admin

from .models import Organization, Request, Station, Metodic,Right,Role,User,Equipment,CompleteStatus,StageStatus,JournalStatus, EventsList,PlaningExperiment,Experiment,Event,Comment

admin.site.register(Request)# Register your models here.
admin.site.register(Organization)
admin.site.register(Station)
admin.site.register(Metodic)
admin.site.register(Right)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Equipment)
admin.site.register(CompleteStatus)
admin.site.register(StageStatus)
admin.site.register(JournalStatus)
admin.site.register(EventsList)
admin.site.register(PlaningExperiment)
admin.site.register(Experiment)
admin.site.register(Event)
admin.site.register(Comment)