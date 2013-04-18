"""Defaults urls for limeade cloud"""
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns


urlpatterns = patterns('',
    url(r'^', include('limeade.cloud.urls.instance')),
    url(r'^', include('limeade.cloud.urls.vnc')),
    url(r'^', include('limeade.cloud.urls.api')),
    url(r'^', include('limeade.cloud.urls.ssh')),
    url(r'^', include('limeade.cloud.urls.export')),
#   url(r'^', include('limeade.cloud.urls.node')),
)
