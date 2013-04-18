from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns('limeade.cloud.views.export',
	url(r'^export/lmds/(?P<slug>[^/]+)/$', 'lmds_export',     name='limeade_cloud_lmds_export'),
)

