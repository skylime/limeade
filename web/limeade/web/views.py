"""Views for limeade web"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from IPy import IP
from limeade.system.utils import get_domains
from limeade.cluster.models import Region
from models import VHost, DefaultVHost, SSLCert, PoolIP, HTTPRedirect as Redirect
from forms import VHostForm, VHostEditForm, RedirectForm, PoolIPForm, SSLCertForm


@login_required
def vhost_list(request):
    """List of web-vhosts.
    
    :param request: the request object
    
    :returns: list of web vhosts
    """
    domains = get_domains(request.user)
    return object_list(request, VHost.objects.filter(domain__in = domains), template_name='limeade_web/vhost_list.html')


@login_required
def vhost_add(request):
    """Create a new web-vhost.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = VHostForm(request.POST or None)
    form.fields['domain'].queryset = get_domains(request.user)
    if form.is_valid():
        form.save()
        return redirect('limeade_web_vhost_list')
    return render_to_response("limeade_web/vhost_add.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required 
def vhost_edit(request, slug):
    """Edit details of a web-vhost.
    
    :param request: the request object
    :param slug: the id of the vhost
    
    :returns: an edit form template
    """
    account = VHost.objects.get(pk=slug)
    form = VHostEditForm(request.POST or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('limeade_web_vhost_list')
    return render_to_response("limeade_web/vhost_edit.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required
def vhost_delete(request, slug):
    """Remove a web-vhost.
    
    :param request: the request object
    :param slug: the id of the vhost
    
    :returns: redirects to vhost list
    """
    v = get_object_or_404(VHost, pk = slug)
    if v.domain.owner() == request.user:
        v.delete()
    return redirect('limeade_web_vhost_list')


@login_required
def vhost_catchall_set(request, slug):
    """Set this vhost as catch-all for the domain.
    
    :param request: the request object
    :param slug: the id of the vhost
    
    :returns: redirects to vhost list
    """
    v = get_object_or_404(VHost, pk = slug)
    if v.domain.owner() == request.user:
        DefaultVHost(vhost=v, domain=v.domain).save()
    return redirect('limeade_web_vhost_list')


@login_required
def vhost_catchall_delete(request, slug):
    """Disable catch-all for this domain.
    
    :param request: the request object
    :param slug: the id of the vhost
    
    :returns: redirects to vhost list
    """
    v = get_object_or_404(DefaultVHost, pk = slug)
    if v.domain.owner() == request.user:
        v.delete()
    return redirect('limeade_web_vhost_list')


@login_required
def redirect_list(request):
    """List HTTP redirects.
    
    :param request: the request object
    
    :returns: list of http redirects
    """
    domains = get_domains(request.user)
    return object_list(request, Redirect.objects.filter(domain__in = domains), template_name='limeade_web/redirect_list.html')


@login_required
def redirect_add(request):
    """Create a new HTTP redirect.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = RedirectForm(request.POST or None)
    form.fields['domain'].queryset = get_domains(request.user)
    if form.is_valid():
        form.save()
        return redirect('limeade_web_redirect_list')
    return render_to_response("limeade_web/redirect_add.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required 
def redirect_edit(request, slug):
    """Edit a HTTP redirect.
    
    :param request: the request object
    :param slug: the id of the redirect
    
    :returns: an edit form template
    """
    r = Redirect.objects.get(pk=slug)
    form = RedirectForm(request.POST or None, instance=r)
    form.fields['domain'].queryset = get_domains(request.user)
    if form.is_valid():
        form.save()
        return redirect('limeade_web_redirect_list')
    return render_to_response("limeade_web/redirect_edit.html",
        {"form": form}, context_instance = RequestContext(request))

@login_required
def redirect_delete(request, slug):
    """Remove a HTTP Redirect.
    
    :param request: the request object
    :param slug: the id of the redirect
    
    :returns: redirect to http redirects list
    """
    r = get_object_or_404(Redirect, pk = slug)
    if r.domain.owner() == request.user:
        r.delete()
    return redirect('limeade_web_redirect_list')    


@login_required
def poolip_list(request):
    """Lists IP addresses.
    
    :param request: the request object
    
    :returns: ip address pool template
    """
    stats = []
    for region in Region.objects.all():
        total = PoolIP.objects.filter(region=region).count()
        free  = PoolIP.objects.filter(region=region, sslcert=None).count()
        used  = total - free
        use   = used / float(total) * 100 if total else 0
        stats += [{'region': region.name, 'total': total, 'used': used, 'free': free, 'use': use}]
    
    total = PoolIP.objects.all().count()
    free  = PoolIP.objects.filter(sslcert=None).count()
    used  = total - free
    use   = used / float(total) * 100 if total else 0
    stats += [{'region': 'Global', 'total': total, 'used': used, 'free': free, 'use': use}]
    return render_to_response("limeade_web/poolip_list.html",
        {"stats": stats}, context_instance = RequestContext(request))


@login_required
def poolip_add(request):
    """Adds an IP address.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = PoolIPForm(request.POST or None)
    if form.is_valid():
        for ip in IP(form.cleaned_data['subnet']):
            PoolIP(ip=str(ip), region=form.cleaned_data['region']).save()
        return redirect('limeade_web_poolip_list')
    return render_to_response("limeade_web/poolip_add.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required
def sslcert_list(request):
    """List a users SSL certificates.
    
    :param request: the request object
    
    :returns: a list of ssl certificates
    """
    return object_list(request, SSLCert.objects.filter(owner = request.user), template_name='limeade_web/sslcert_list.html')

@login_required
def sslcert_add(request):
    """Add a new SSL certificate.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = SSLCertForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        c = SSLCert()
        c.owner = request.user
        c.ip = PoolIP.objects.filter(sslcert=None)[0]
        if c.ip:
            c.set_cert(request.FILES['cert'].read(), request.FILES['key'].read(), request.FILES['ca'].read())
            c.save()
        else:
            pass # TODO: fail better
        return redirect('limeade_web_sslcert_list')
    return render_to_response("limeade_web/sslcert_add.html",
        {"form": form}, context_instance = RequestContext(request))

@login_required
def sslcert_delete(request, slug):
    """Remove a SSL certificate.
    
    :param request: the request object
    :param slug: the id of the ssl cert
    
    :returns: redirects to ssl cert list
    """
    cert = get_object_or_404(SSLCert, pk = slug)
    if cert.owner == request.user:
        cert.delete()
    return redirect('limeade_web_sslcert_list') 

