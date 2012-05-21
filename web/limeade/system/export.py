from django.http import HttpResponse
from django.conf import settings

from .utils import export_header
from .models import Person


def user_export(request):
    response = HttpResponse(mimetype='text/plain')
    response.write(export_header())
    user_tpl  = "$system_user = {\n"
    group_tpl = "$system_group = {\n"
    for p in Person.objects.all():
        username = p.system_user_name()
        home     = p.system_user_home()
        uid      = p.system_user_id()
        user_tpl  += "\t'%s' => { ensure => present, uid => %s, gid => %s, shell => '/bin/false', home => '%s', managehome => true, require => Group['%s'] }\n"
        group_tpl += "\t'%s' => { ensure => present, gid => %s }\n"
    user_tpl  += "}\n"
    group_tpl += "}\n"
    response.write(user_tpl  % (username, uid, uid, home, username))
    response.write(group_tpl % (username, uid))
    return response

