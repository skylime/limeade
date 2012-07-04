"""SSH urls for limeade cloud"""
from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns('limeade.cloud.views.ssh',
    url(r'^sshkey/$',                       'sshkey_list',   name='limeade_cloud_sshkey_list'),
    url(r'^sshkey/add/$',                   'sshkey_add',    name='limeade_cloud_sshkey_add'),
    url(r'^sshkey/(?P<slug>[^/]+)/delete$', 'sshkey_delete', name='limeade_cloud_sshkey_delete'),
)

