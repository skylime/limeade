from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
	url(r'^vhost/$',                          vhost_list,   name='limeade_web_vhost_list'),
	url(r'^vhost/add/$',                      vhost_add,    name='limeade_web_vhost_add'),
	url(r'^vhost/(?P<slug>[^/]+)/$',          vhost_edit,   name='limeade_web_vhost_edit'),
	url(r'^vhost/(?P<slug>[^/]+)/delete$',    vhost_delete, name='limeade_web_vhost_delete'),

	url(r'^redirect/$',                       redirect_list,   name='limeade_web_redirect_list'),
	url(r'^redirect/add/$',                   redirect_add,    name='limeade_web_redirect_add'),
	url(r'^redirect/(?P<slug>[^/]+)/$',       redirect_edit,   name='limeade_web_redirect_edit'),
	url(r'^redirect/(?P<slug>[^/]+)/delete$', redirect_delete, name='limeade_web_redirect_delete'),

	url(r'^cert/$',                           sslcert_list,   name='limeade_web_sslcert_list'),
	url(r'^cert/add/$',                       sslcert_add,    name='limeade_web_sslcert_add'),
	url(r'^cert/(?P<slug>[^/]+)/delete$',     sslcert_delete, name='limeade_web_sslcert_delete'),

)