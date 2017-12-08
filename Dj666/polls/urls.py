from django.conf.urls import url,include
from polls import views
from .admin import admin_site



urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin_site.urls)),

    url(r'^newuser$', views.newuser, name='newuser'),
    url(r'^ls$', views.IndexView.as_view(), name='ls'),
    # url(r'^details/(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),
    url(r'^details/(?P<id>[0-9]+)$', views.DetailView.as_view(), name='details'),

    # url(r'^details/(?P<id>[0-9]+)(/(?P<pd>[0-9]+))*$', views.DetailView.as_view(), name='details'),
    # url(r'^details/([0-9]+)/([0-9]+)*$', views.DetailView.as_view(),  {'foo': 'bar'},name='details'),


    url(r'^getcar/(?P<id>[0-9]+)$', views.getcar, name='getcar'),
]