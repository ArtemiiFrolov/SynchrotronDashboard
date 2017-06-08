from django.contrib import admin

from .models import *


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    class ExperimentsInline(admin.TabularInline):
        model = Experiment
        extra = 0

    list_display = ('name', 'author', 'station', 'start', 'end')
    list_filter = ('author', 'station', 'start')
    search_fields = ['name', 'station__name']
    inlines = [ExperimentsInline, ]


admin.site.register(Organization)
admin.site.register(Station)
admin.site.register(Approach)
admin.site.register(Right)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Equipment)
admin.site.register(CompleteStatus)
admin.site.register(StageStatus)
admin.site.register(JournalStatus)
admin.site.register(EventsList)
admin.site.register(ExperimentPlan)
admin.site.register(Experiment)
admin.site.register(Event)
admin.site.register(Comment)
