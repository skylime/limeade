from django.conf.urls.defaults import *
from views import *
import export

urlpatterns = patterns('',
	url(r'^account/$',                       account_list,   name='limeade_mail_account_list'),
	url(r'^account/add/$',                   account_add,    name='limeade_mail_account_add'),
	url(r'^account/(?P<slug>[^/]+)/$',       account_edit,   name='limeade_mail_account_edit'),
	url(r'^account/(?P<slug>[^/]+)/delete$', account_delete, name='limeade_mail_account_delete'),

	url(r'^redirect/$',                       redirect_list,   name='limeade_mail_redirect_list'),
	url(r'^redirect/add/$',                   redirect_add,    name='limeade_mail_redirect_add'),
	url(r'^redirect/(?P<slug>[^/]+)/$',       redirect_edit,   name='limeade_mail_redirect_edit'),
	url(r'^redirect/(?P<slug>[^/]+)/delete$', redirect_delete, name='limeade_mail_redirect_delete'),
	
	(r'^export/account.csv',  export.account_export),
	(r'^export/redirect.csv', export.redirect_export),
	(r'^export/route.csv',    export.route_export),
)