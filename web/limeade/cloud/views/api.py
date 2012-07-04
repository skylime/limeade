"""Views for limeade cloud API calls"""
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from anyjson import serialize

from limeade.cloud.models import Instance


def instance_activate(request):
    if request.GET.get('site_api_key', '') != settings.SITE_API_KEY:
        return HttpResponse(serialize({
            "status": "failure",
            "reason": 'wrong key'
        }), mimetype="application/json")
    
    i = get_object_or_404(Instance, pk=request.GET['instance'])
    i.active = True
    i.save()
    
    response = {
        "status": "success",
        "retval": i.domain
    }
    
    return HttpResponse(serialize(response), mimetype="application/json")


def instance_info(request, slug):
    i = get_object_or_404(Instance, mac_addr=slug)
    
    response = {'hostname': i.hostname}
    response['ssh_keys'] = [k.key for k in i.sshkeys.all()]
    
    return HttpResponse(serialize(response), mimetype="application/json")

