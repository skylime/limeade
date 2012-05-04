from django.conf.urls.defaults import *
from django.conf import settings


# Serve static files
urlpatterns = patterns('',
    url(r'^media/(?P<path>lib/.*)$', 'django.views.static.serve', {'document_root': settings.LIB_MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$',     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$',     'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^js/i18n\.js$',            'django.views.i18n.javascript_catalog', name='js_i18n'),
)

# Project related urls
urlpatterns += patterns('',
    url(r'^admin/',   include('limeade.admin_urls')),
    url(r'^system/',  include('limeade.system.urls')),
	url(r'^web/',     include('limeade.web.urls')),
	url(r'^mail/',    include('limeade.mail.urls')),
	url(r'^cloud/',   include('limeade.cloud.urls')),
	url(r'^mysql/',   include('limeade.mysql.urls')),
	url(r'^ftp/',     include('limeade.ftp.urls')),
	url(r'^cluster/', include('limeade.cluster.urls')),
)

# Account administer
urlpatterns += patterns('',
	url(r'^accounts/login/$',                'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$',               'django.contrib.auth.views.logout_then_login'),
	url(r'^accounts/change_password/$',      'django.contrib.auth.views.password_change'),
	url(r'^accounts/change_password/done/$', 'django.contrib.auth.views.password_change_done'),
)
