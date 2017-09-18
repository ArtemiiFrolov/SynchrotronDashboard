from django.conf.urls import url, include
from django.conf.urls import url

from . import views
from main.api import urls as api_urls

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
    url(r'^application_row_disapprove/(?P<pk>.*)/$', views.application_row_disapprove, name='application_row_disapprove'),
    url(r'^modal_show/(?P<pk>.*)/$', views.modal_show, name='modal_show'),
    url(r'^comment_from_application/(?P<pk>.*)/$', views.comment_from_application, name='comment_from_application'),
    url(r'^comment_from_modal/(?P<pk>.*)/$', views.comment_from_modal, name='comment_from_modal'),

    url(r'^stations/(?P<pk>.*)/$', views.station_view, name='station'),

    url(r'^users/(?P<user_id>.*)/$', views.user_view, name='user'),
    url(r'^all_users/$', views.all_users, name='all_users'),

    url(r'^organizations/(?P<pk>.*)/$', views.organization_view, name='organization'),

    url(r'^planning_experiments/$', views.planning_experiments, name='planning_experiments'),
    url(r'^planned_experiments/$', views.planned_experiments, name='planned_experiments'),
    url(r'^planned_table$', views.planned_table, name='planned_table'),
    url(r'^planning_calendar/$', views.planning_calendar, name='planning_calendar'),

    url(r'^journal/$', views.journal, name='journal'),
    url(r'^journal/new$', views.journal_new, name='journal_new'),

    url(r'^synchrotron_calendar/$', views.synchrotron_calendar, name='synchrotron_calendar'),
    url(r'^delete_event/$', views.delete_event, name='delete_event'),

    url(r'^api/', include(api_urls.urls, namespace='api')),
]
