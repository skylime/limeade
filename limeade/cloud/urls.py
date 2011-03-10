from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
	url(r'^instance/$',                         instance_list,     name='limeade_cloud_instance_list'),
	url(r'^instance/add/$',                     instance_add,      name='limeade_cloud_instance_add'),
	#url(r'^instance/(?P<slug>[^/]+)/$',         instance_edit,     name='limeade_cloud_instance_edit'),
	url(r'^instance/(?P<slug>[^/]+)/delete$',   instance_delete,   name='limeade_cloud_instance_delete'),
	url(r'^instance/(?P<slug>[^/]+)/start$',    instance_start,    name='limeade_cloud_instance_start'),
	url(r'^instance/(?P<slug>[^/]+)/stop$',     instance_stop,     name='limeade_cloud_instance_stop'),
	url(r'^instance/(?P<slug>[^/]+)/restart$',  instance_restart,  name='limeade_cloud_instance_restart'),
	
	url(r'^api/activate$',                      instance_activate, name='limeade_cloud_instance_activate'),
	url(r'^api/info/(?P<slug>[^/]+)/$',        instance_info,     name='limeade_cloud_instance_info'),
	#url(r'^instance/(?P<slug>[^/]+)/vnc/$',     instance_vnc,     name='limeade_cloud_instance_vnc'),
	
	url(r'^sshkey/$',                         sshkey_list,     name='limeade_cloud_sshkey_list'),
	url(r'^sshkey/add/$',                     sshkey_add,      name='limeade_cloud_sshkey_add'),
	url(r'^sshkey/(?P<slug>[^/]+)/delete$',   sshkey_delete,   name='limeade_cloud_sshkey_delete'),

#	url(r'^node/$',                       node_list,   name='limeade_cloud_node_list'),
#	url(r'^node/add/$',                   node_add,    name='limeade_cloud_node_add'),
#	url(r'^node/(?P<slug>[^/]+)/$',       node_edit,   name='limeade_cloud_node_edit'),
#	url(r'^node/(?P<slug>[^/]+)/delete$', node_delete, name='limeade_cloud_node_delete'),
)