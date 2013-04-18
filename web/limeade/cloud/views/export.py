from django.http import HttpResponse
import csv
from limeade.cloud.models import Instance

def lmds_export(request, slug):
	response = HttpResponse(mimetype='text/csv')
	w = csv.writer(response)
	for i in Instance.objects.filter(node__region__name=slug):
		w.writerow([i.pk, i.hostname, i.mac_addr, i.ip, ""])
	
	return response
