"""VNC urls for limeade cloud"""
from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns('limeade.cloud.views.vnc',
    url(r'^instance/(?P<slug>[^/]+)/vnc/$',              'instance_vnc',     name='limeade_cloud_instance_vnc'),
    url(r'^instance/(?P<slug>[^/]+)/(?P<token>[^/]+)/$', 'instance_vnc_auth', name='limeade_cloud_instance_vnc_auth'),
)

