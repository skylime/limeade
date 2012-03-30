from django.conf.urls.defaults import *
from views import *
import export

urlpatterns = patterns('',
	url(r'^account/$',                       account_list,   name='limeade_ftp_account_list'),
	url(r'^account/add/$',                   account_add,    name='limeade_ftp_account_add'),
	url(r'^account/(?P<slug>[^/]+)/$',       account_edit,   name='limeade_ftp_account_edit'),
	url(r'^account/(?P<slug>[^/]+)/delete$', account_delete, name='limeade_ftp_account_delete'),
	(r'^export/account.csv', export.export),
)