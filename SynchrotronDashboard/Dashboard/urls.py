from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^requests/(?P<request_serial>.*)/$', views.show_request, name='show_request'),
    url(r'^requests/$', views.create_request, name='create_request'),
    url(r'^show_all_requests/$', views.show_all_requests, name='show_all_requests'),
]