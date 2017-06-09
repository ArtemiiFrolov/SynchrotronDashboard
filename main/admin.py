from django.contrib import admin

from .models import *


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    class ExperimentsInline(admin.TabularInline):
        model = Experiment
        extra = 0

    class ExperimentPlanInline(admin.TabularInline):
        model = ExperimentPlan
        extra = 0

    list_display = ('name', 'author', 'station', 'start', 'end')
    list_filter = ('author', 'station', 'start', 'complete_status', 'stage_status')
    search_fields = ['name', 'station__name', 'complete_status__name', 'stage_status__name']
    inlines = [ExperimentPlanInline, ExperimentsInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    class UserInline(admin.TabularInline):
        model = User.organization.through
        extra = 0

    class ApplicationInline(admin.TabularInline):
        model = Application.organizations.through
        extra = 0

    search_fields = ['name']
    inlines = [UserInline, ApplicationInline]


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    class UserInline(admin.TabularInline):
        model = User.station.through
        extra = 0

    class ApplicationInline(admin.TabularInline):
        model = Application
        extra = 0

    class ExperimentPlanInline(admin.TabularInline):
        model = ExperimentPlan
        extra = 0

    class ExperimentsInline(admin.TabularInline):
        model = Experiment
        extra = 0

    list_display = ('name', 'short_description')
    search_fields = ['name']
    inlines = [UserInline,
               ApplicationInline,
               ExperimentPlanInline,
               ExperimentsInline]


@admin.register(Approach)
class ApproachAdmin(admin.ModelAdmin):
    class ApplicationInline(admin.TabularInline):
        model = Application.approaches.through
        extra = 0

    class ExperimentInline(admin.TabularInline):
        model = Experiment
        extra = 0

    search_fields = ['name']
    inlines = [ApplicationInline, ExperimentInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class ExperimentsInline(admin.TabularInline):
        model = Experiment
        fk_name = 'author'
        extra = 0

    class ExperimentPlanInline(admin.TabularInline):
        model = ExperimentPlan
        fk_name = 'author'
        extra = 0

    class ApplicationInline(admin.TabularInline):
        model = Application
        fk_name = 'author'
        extra = 0

    list_display = ('email', 'name', 'role')
    list_filter = ['station']
    search_fields = ['name', 'station__name']
    inlines = [ExperimentPlanInline, ExperimentsInline, ApplicationInline]


@admin.register(ExperimentPlan)
class ExperimentPlanAdmin(admin.ModelAdmin):
    list_display = ( 'application', 'author', 'start', 'end', 'status', 'station')
    list_filter = ('station', 'status', 'author', 'application')
    search_fields = ['station__name', 'author__name', 'status__name']


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('application', 'author', 'start', 'end', 'operator', 'comment')
    list_filter = ('station', 'author', 'operator')
    search_fields = ['station__name', 'author__name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('application', 'author', 'text')

admin.site.register(Right)
admin.site.register(Role)
admin.site.register(Equipment)
admin.site.register(CompleteStatus)
admin.site.register(StageStatus)
admin.site.register(JournalStatus)
admin.site.register(EventsList)