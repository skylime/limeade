from django.http import HttpResponse
import csv
from models import Server

def export(request):
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
	
	
	

