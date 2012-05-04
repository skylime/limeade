from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import os.path


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(admin.__file__), 'media')}),
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    url(r'^',     include(admin.site.urls)),
)

