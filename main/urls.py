from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login_view, name='login'),
    url(r'^test$', views.test_view, name='test'),

    url(r'^applications/(?P<request_serial>.*)/$', views.application_view, name='application'),
    url(r'^applications/new$', views.application_form_view, name='application_form'),
    url(r'^applications/$', views.applications_view, name='applications'),

    url(r'^stations/(?P<station_short>.*)/$', views.station_view, name='station'),

    url(r'^users/(?P<user_id>.*)/$', views.user_view, name='user'),
    url(r'^users/$', views.users_view, name='users'),
]
