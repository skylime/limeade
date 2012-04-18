from django.http import HttpResponse
from django.conf import settings
from limeade.cluster.models import Server
from limeade.system.utils import export_header
from models import *
import zipfile
import csv

def vhost_export(request):
	response = HttpResponse(mimetype='text/plain')
	response.write(export_header())
	tpl = """
	'{vhost}' => {{
		'home'     => '{home}',
		'user'     => '{user}',
		'group'    => '{user}',
		'aliases'  => {aliases},
	}},
"""
	for style in VHOST_STYLES:
		response.write("$web_" + style[0] + "_vhosts = {")
		for v in VHost.objects.filter(style=style[0]):
			user = v.domain.owner().get_profile()
			response.write(tpl.format(
				vhost    = v.name + '.' + unicode(v.domain),
				user     = user.system_user_name(),
				home     = user.system_user_home(),
				aliases  = ('["*.' + unicode(v.domain) + '"]' if v.defaultvhost_set.exists() else '[]'),
			))

		response.write("}\n")
		
	return response

def ssl_export(request):
	response = HttpResponse(mimetype='application/x-zip')
	response['Content-Disposition'] = 'attachment; filename=web_ssl.zip'
	
	z = zipfile.ZipFile(response, mode='w')
	
	for sslcert in SSLCert.objects.all():
		pk = str(sslcert.pk)
		
		z.writestr('web_ssl/' + pk + '/cert.pem', sslcert.cert)
		z.writestr('web_ssl/' + pk + '/key.pem',  sslcert.key)
		z.writestr('web_ssl/' + pk + '/ca.pem',   sslcert.ca)
		
	return response

def lb_export(request):
	response = HttpResponse(mimetype='text/plain')
	response.write(export_header())
	tpl = """
	'{vhost}' => {{
		'style'    => '{style}',
		'cert_id'  => {cert_id},
		'cert_ip'  => {cert_ip},
	}},
"""
	
	response.write("$web_lb_vhosts = {")
	for v in VHost.objects.all():
		response.write(tpl.format(
			vhost    = ('*' if v.defaultvhost_set.exists() else v.name) + '.' + unicode(v.domain),
			style    = v.style,
			cert_id  = '"' + str(v.cert.pk) + '"' if v.cert else 'undef',
			cert_ip  = '"' + str(v.cert.ip) + '"' if v.cert else 'undef',
		))

	response.write("}\n")
	return response

def redirect_export(request):
	response = HttpResponse(mimetype='text/plain')
	response.write(export_header())
	response.write("$web_redirects = {\n")
	for r in HTTPRedirect.objects.all():
		response.write('"{vhost}" => {{ "target" => "{to}", }},\n'.format(
			vhost = r.name + '.' + unicode(r.domain),
			to    = r.to,
		))
	
	response.write("}\n")
	return response
	
