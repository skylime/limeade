"""Views for limeade cloud SSH Keys"""
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.template import RequestContext

from limeade.cloud.forms import SSHKeyForm
from limeade.cloud.models import SSHKey


@login_required
def sshkey_list(request):
    """Show a list of the Users SSH Keys.
    
    :param request: the request object
    
    :returns: a list of ssh keys
    """
    return object_list(request, SSHKey.objects.filter(owner=request.user), 
        template_name='limeade_cloud/sshkey_list.html')


@login_required
def sshkey_add(request):
    """Form to add a new SSH Key.
    
    :param request: the request object
    
    :returns: an edit form template
    """
    form = SSHKeyForm(request.POST or None)
    
    if form.is_valid():
        key = form.save(commit=False)
        key.owner = request.user
        key.save()
        return redirect('limeade_cloud_sshkey_list')
    
    return render_to_response("limeade_cloud/sshkey_add.html",
        {"form": form}, context_instance=RequestContext(request))


@login_required
def sshkey_delete(request, slug):
    """Delete a SSH Key.
    
    :param request: the request object
    :param slug: the id of the ssh key
    
    :returns: redirect to a list of ssh keys
    """
    key = get_object_or_404(SSHKey, pk=slug)
    if key.owner == request.user:
        key.delete()
    
    return redirect('limeade_cloud_sshkey_list')

