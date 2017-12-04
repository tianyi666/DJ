"""Dj666 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,handler404
from django.contrib import admin
from polls import  views
from django.views.static import serve
from .settings import MEDIA_ROOT
from django.views.generic import TemplateView,RedirectView
from django.core.urlresolvers import reverse_lazy


extra_patterns = [
    url(r'^$', views.index),
    url(r'^ls$', views.IndexView.as_view(), name='ls'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="404.html")),
    # url(r'^redirect',RedirectView.as_view(url='polls/ls')),
    url(r'^redirect',RedirectView.as_view(url=reverse_lazy('polls:ls'))), #因为此时还没创建所以用lazy模式
    # url(r'^polls/', include(extra_patterns)),

    # url(r'^polls/', include([
    #     url(r'^$', views.index),
    #     url(r'^ls$', views.IndexView.as_view(), name='ls'),
    # ])),



    url(r'^polls/',include('polls.urls',namespace='polls') ),
    url(r'^vft/',include('vft.urls',namespace='vft') ),

    #访问上传的文件
    url(r'^upload/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
]

handler404='views.error'
