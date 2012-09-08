"""Views for limeade cluster"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from models import Server, Service, Region
from forms import ServerForm, RegionForm


@login_required
def server_list(request):
    """Show a list of servers.
    
    :param request: the request object
    
    :returns: a list of servers
    """
    return object_list(request, Server.objects.all(),
            template_name='limeade_cluster/server_list.html')


@login_required
def server_add(request):
    """Add a new server to the cluster.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = ServerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('limeade_cluster_server_list')
    return render_to_response("limeade_cluster/server_add.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required 
def server_edit(request, slug):
    """Edit a server.
    
    :param request: the request object
    :param slug: the id of the server
    
    :returns: an edit form template
    """
    server = Server.objects.get(pk=slug)
    form = ServerForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('limeade_cluster_server_list')
    return render_to_response("limeade_cluster/server_edit.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required
def server_enable(request, slug):
    """Enable a server after a maintenance is over.
    
    :param request: the request object
    :param slug: the id of the server
    
    :returns: redirect to server list
    """
    s = get_object_or_404(Server, pk = slug)
    s.enabled = True
    s.save()
    return redirect('limeade_cluster_server_list')


@login_required
def server_disable(request, slug):
    """Put a server into maintenance.
    
    :param request: the request object
    :param slug: the id of the server
    
    :returns: redirect to server list
    """
    s = get_object_or_404(Server, pk = slug)
    s.enabled = False
    s.save()
    return redirect('limeade_cluster_server_list')


@login_required
def server_delete(request, slug):
    """Remove a server from the cluster.
    
    :param request: the request object
    :param slug: the id of the server
    
    :returns: redirect to server list
    """
    s = get_object_or_404(Server, pk = slug)
    s.delete()
    return redirect('limeade_cluster_server_list')


@login_required
def region_list(request):
    """Show a list of regions.
    
    :param request: the request object
    
    :returns: a list of regions
    """
    return object_list(request, Region.objects.all(),
            template_name='limeade_cluster/region_list.html')


@login_required
def region_add(request):
    """Add a new region to the cluster.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = RegionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('limeade_cluster_region_list')
    return render_to_response("limeade_cluster/region_add.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required
def region_edit(request, slug):
    """Edit a region.
    
    :param request: the request object
    :param slug: the id of the region
    
    :returns: an edit form template
    """
    region = Region.objects.get(pk=slug)
    form = RegionForm(request.POST or None, instance=region)
    if form.is_valid():
        form.save()
        return redirect('limeade_cluster_region_list')
    return render_to_response("limeade_cluster/region_edit.html",
        {"form": form}, context_instance = RequestContext(request))


@login_required
def region_delete(request, slug):
    """Remove a region from the cluster
    
    :param request: the request object
    :param slug: the id of the region
    
    :returns: redirect to list of regions
    """
    s = get_object_or_404(Server, pk = slug)
    s.delete()
    return redirect('limeade_cluster_region_list')

