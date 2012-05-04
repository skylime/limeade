from django.conf.urls.defaults import *
from views import *
import export

urlpatterns = patterns('',
	url(r'^server/$',                        server_list,    name='limeade_cluster_server_list'),
	url(r'^server/add/$',                    server_add,     name='limeade_cluster_server_add'),
	url(r'^server/(?P<slug>[^/]+)/$',        server_edit,    name='limeade_cluster_server_edit'),
	url(r'^server/(?P<slug>[^/]+)/enable$',  server_enable,  name='limeade_cluster_server_enable'),
	url(r'^server/(?P<slug>[^/]+)/disable$', server_disable, name='limeade_cluster_server_disable'),
	url(r'^server/(?P<slug>[^/]+)/delete$',  server_delete,  name='limeade_cluster_server_delete'),
	url(r'^region/$',                        region_list,    name='limeade_cluster_region_list'),
	url(r'^region/add/$',                    region_add,     name='limeade_cluster_region_add'),
	url(r'^region/(?P<slug>[^/]+)/$',        region_edit,    name='limeade_cluster_region_edit'),
	url(r'^region/(?P<slug>[^/]+)/delete$',  region_delete,  name='limeade_cluster_region_delete'),
	(r'^export/nodes.pp', export.nodes),
	(r'^export/variables.pp', export.variables),
)