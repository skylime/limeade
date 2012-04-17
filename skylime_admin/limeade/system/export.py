from django.http import HttpResponse
from django.conf import settings
from limeade.system.utils import export_header
from models import Person

def user_export(request):
	response = HttpResponse(mimetype='text/plain')
	response.write(export_header())
	for p in Person.objects.all():
		username = p.system_user_name()
		home     = p.system_user_home()
		uid      = p.system_user_id()
		user_tpl  = "user  { '%s': ensure => present, uid => %s, gid => %s, shell => '/bin/false', home => '%s', managehome => true, require => Group['%s'] }\n"
		group_tpl = "group { '%s': ensure => present, gid => %s }\n"
		response.write(user_tpl  % (username, uid, uid, home, username))
		response.write(group_tpl % (username, uid))
	return response
