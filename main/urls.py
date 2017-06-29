from django.conf.urls import url, include
from rest_framework import routers

from . import views
from main.api import viewsets

api_router = routers.DefaultRouter()
api_router.register(r'stations', viewsets.StationViewSet, base_name='station')

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

    url(r'^api/', include(api_router.urls, namespace='api')),
]


