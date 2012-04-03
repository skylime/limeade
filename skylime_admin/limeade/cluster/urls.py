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
	(r'^export/nodes.pp', export.nodes),
	(r'^export/variables.pp', export.variables),
)