"""API urls for limeade cloud"""
from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns('limeade.cloud.views.api',
    url(r'^api/activate$',              'instance_activate', name='limeade_cloud_instance_activate'),
    url(r'^api/info/(?P<slug>[^/]+)/$', 'instance_info',     name='limeade_cloud_instance_info'),
)

