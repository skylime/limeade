from django.http import HttpResponse
import csv
from models import Account, Redirect
from limeade.cluster.models import Server
from django.conf import settings

def account_export(request):
	response = HttpResponse(mimetype='text/csv')
	w = csv.writer(response)
	for a in Account.objects.all():
		w.writerow([a.name + '@' + a.domain.name, a.password])
		
	return response


def redirect_export(request):
	response = HttpResponse(mimetype='text/csv')
	w = csv.writer(response)
	for r in Redirect.objects.all():
		w.writerow([r.name + '@' + r.domain.name, r.to])
		
	return response


def route_export(request):
	response = HttpResponse(mimetype='text/csv')
	w = csv.writer(response)
	destinations = Server.objects.filter(services__name=settings.MAIL_POSTBOX_SERVICE_NAME, enabled=True)
	for a in Account.objects.all():
		for d in destinations:
			w.writerow([a.name + '@' + a.domain.name, d.ip])
		
	return response
