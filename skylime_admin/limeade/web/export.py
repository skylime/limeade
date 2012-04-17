from django.http import HttpResponse
from django.conf import settings
from limeade.cluster.models import Server
from limeade.system.utils import export_header
from models import *

def vhost_export(request):
	response = HttpResponse(mimetype='text/plain')
	response.write(export_header())
	tpl = """
	'{vhost}' => {{
		'home'  => '{home}',
		'user'  => '{user}',
		'group' => '{user}',
	}},
"""
	for style in VHOST_STYLES:
		response.write("$web_" + style[0] + "_vhosts = {")
		for v in VHost.objects.filter(style=style[0]):
			user = v.domain.owner().get_profile()
			response.write(tpl.format(
				vhost = v.name + '.' + unicode(v.domain),
				user  = user.system_user_name(),
				home  = user.system_user_home()
			))

		response.write("}\n")
		
	return response

