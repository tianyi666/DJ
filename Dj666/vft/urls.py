from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^details/(?P<pk>[0-9]+)$', views.DogDetailView.as_view(),name='dogdetails'),
    url(r'^reg2/', views.register),
    url(r'^dogls/', views.DogLsView.as_view()),
    url(r'^dognew/', views.DogCreateView.as_view()),
    url(r'^dogupd/(?P<pk>[0-9]+)',views.DogUpdateView.as_view()),
    url(r'^dogmix/(?P<id>[0-9]+)',views.DogMixView.as_view()),

    url(r'^reg/', views.reg),
    url(r'^dogform/', views.dogform),
    url(r'^formset/', views.formset),

    url(r'^dogs/(?P<pk>[0-9]+)$', views.DogDetailView.as_view())
    ]