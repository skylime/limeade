from django.http import HttpResponse
import csv
from models import Account

def export(request):
	response = HttpResponse(mimetype='text/csv')
	w = csv.writer(response)
	for a in Account.objects.all():
		w.writerow([a.name, a.password, a.vhost.domain, unicode(a.vhost)])
		
	return response
	
	
	

