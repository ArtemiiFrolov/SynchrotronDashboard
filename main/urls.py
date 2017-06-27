from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^test$', views.test_view, name='test'),

    url(r'^applications/(?P<serial>.*)/$', views.application_view, name='application'),
    url(r'^applications/(?P<serial>.*)/edit$', views.application_edit, name='application_edit'),
    url(r'^applications/new$', views.application_edit, name='application_new'),
    url(r'^applications/$', views.applications_view, name='applications'),

    url(r'^stations/(?P<pk>.*)/$', views.station_view, name='station'),

    url(r'^users/(?P<user_id>.*)/$', views.user_view, name='user'),
    url(r'^users/$', views.users_view, name='users'),

    url(r'^organizations/(?P<pk>.*)/$', views.organization_view, name='organization'),

    url(r'^planning_experiments/$', views.planning_experiments, name='planning_experiments'),
    url(r'^planned_experiments/$', views.planned_experiments, name='planned_experiments'),
    url(r'^planning_calendar/$', views.planning_calendar, name='planning_calendar'),

    url(r'^journal/$', views.journal, name='journal'),
    url(r'^journal/new$', views.journal_new, name='journal_new'),
]
