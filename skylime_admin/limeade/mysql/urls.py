from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
	url(r'^db/$',                       db_list,   name='limeade_mysql_db_list'),
	url(r'^db/add/$',                   db_add,    name='limeade_mysql_db_add'),
	url(r'^db/(?P<slug>[^/]+)/$',       db_edit,   name='limeade_mysql_db_edit'),
	url(r'^db/(?P<slug>[^/]+)/delete$', db_delete, name='limeade_mysql_db_delete'),

)