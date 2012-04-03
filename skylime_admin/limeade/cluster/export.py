from django.http import HttpResponse
import csv
from models import Server, Service

def nodes(request):
	response = HttpResponse(mimetype='text/plain')
	
	response.write(
"""
node default {

}

node core-io {
        include users
}

"""
	)

	for s in Server.objects.all():
		
		response.write("node '" + s.hostname + "' inherits core-io {\n")
		for service in s.services.all():
			response.write("\tinclude " + unicode(service) + "\n")
			
		response.write("}\n")
				
	return response
	
	
def variables(request):
	response = HttpResponse(mimetype='text/plain')
	
	for s in Service.objects.all():
		ips       = []
		hostnames = []
		
		for srv in s.server_set.filter(enabled=True):
			ips       += ['"' + srv.ip + '"']
			hostnames += ['"' + srv.hostname + '"']
		
		response.write("$" + unicode(s) + "_nodes_ip   = [" + ', '.join(ips)       + "]\n")
		response.write("$" + unicode(s) + "_nodes_host = [" + ', '.join(hostnames) + "]\n")
		
	return response
	