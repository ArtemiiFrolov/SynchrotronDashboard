from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls import url

from . import views
from main.api import viewsets

api_router = routers.DefaultRouter()
api_router.register(r'stations', viewsets.StationViewSet, base_name='station')
api_router.register(r'organizations', viewsets.OrganizationViewSet, base_name='organization')
api_router.register(r'approaches', viewsets.ApproachViewSet, base_name='approach')
api_router.register(r'rights', viewsets.RightViewSet, base_name='right')
api_router.register(r'roles', viewsets.RoleViewSet, base_name='role')
api_router.register(r'equipment', viewsets.EquipmentViewSet, base_name='equipment')
api_router.register(r'complete_statuses', viewsets.CompleteStatusViewSet, base_name='complete_status')
api_router.register(r'stage_statuses', viewsets.StageStatusViewSet, base_name='stage_status')
api_router.register(r'journal_statuses', viewsets.JournalStatusViewSet, base_name='journal_status')
api_router.register(r'event_lists', viewsets.EventsListViewSet, base_name='event')
api_router.register(r'users', viewsets.UserViewSet, base_name='user')
api_router.register(r'applications', viewsets.ApplicationViewSet, base_name='application')
api_router.register(r'experiment_plans', viewsets.ExperimentPlanViewSet, base_name='experiment_plan')
api_router.register(r'experiments', viewsets.ExperimentViewSet, base_name='experiment')
api_router.register(r'events', viewsets.EventViewSet, base_name='event')
api_router.register(r'comment', viewsets.CommentViewSet, base_name='comment')
api_router.register(r'application_counter', viewsets.ApplicationCounterViewSet, base_name='application_counter')


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^test$', views.test_view, name='test'),

    url(r'^applications/(?P<serial>.*)/$', views.application_view, name='application'),
    url(r'^applications/(?P<serial>.*)/edit$', views.application_edit, name='application_edit'),
    url(r'^applications/new$', views.application_edit, name='application_new'),
    url(r'^applications/$', views.applications_view, name='applications'),
    url(r'^applications_table$', views.applications_table, name='applications_table'),
    url(r'^application_row/(?P<pk>.*)/$', views.application_row, name='application_row'),

    url(r'^stations/(?P<pk>.*)/$', views.station_view, name='station'),

    url(r'^users/(?P<user_id>.*)/$', views.user_view, name='user'),
    url(r'^users/$', views.users_view, name='users'),

    url(r'^organizations/(?P<pk>.*)/$', views.organization_view, name='organization'),

    url(r'^planning_experiments/$', views.planning_experiments, name='planning_experiments'),
    url(r'^planned_experiments/$', views.planned_experiments, name='planned_experiments'),
    url(r'^planning_calendar/$', views.planning_calendar, name='planning_calendar'),

    url(r'^journal/$', views.journal, name='journal'),
    url(r'^journal/new$', views.journal_new, name='journal_new'),

    url(r'^api/', include(api_router.urls, namespace='api')),
]
