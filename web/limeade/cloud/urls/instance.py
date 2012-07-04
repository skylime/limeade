"""Instance urls for limeade cloud"""
from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns('limeade.cloud.views.instance',
    url(r'^instance/$',                        'instance_list',    name='limeade_cloud_instance_list'),
    url(r'^instance/add/$',                    'instance_add',     name='limeade_cloud_instance_add'),
    #url(r'^instance/(?P<slug>[^/]+)/$',       'instance_edit',    name='limeade_cloud_instance_edit'),
    url(r'^instance/(?P<slug>[^/]+)/delete$',  'instance_delete',  name='limeade_cloud_instance_delete'),
    url(r'^instance/(?P<slug>[^/]+)/start$',   'instance_start',   name='limeade_cloud_instance_start'),
    url(r'^instance/(?P<slug>[^/]+)/stop$',    'instance_stop',    name='limeade_cloud_instance_stop'),
    url(r'^instance/(?P<slug>[^/]+)/restart$', 'instance_restart', name='limeade_cloud_instance_restart'),
)

