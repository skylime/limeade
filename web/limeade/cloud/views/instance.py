"""Views for limeade cloud Instances"""
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q

from celery.execute import send_task

from limeade.cloud.utils import get_best_node
from limeade.cloud.forms import InstanceForm
from limeade.cloud.models import Instance
from limeade.system.models import Product
from limeade.cloud.models import SSHKey

import libvirt


vm_state = {
    libvirt.VIR_DOMAIN_NOSTATE:  None,
    libvirt.VIR_DOMAIN_RUNNING:  'running',
    libvirt.VIR_DOMAIN_BLOCKED:  'blocked',
    libvirt.VIR_DOMAIN_PAUSED:   'paused',
    libvirt.VIR_DOMAIN_SHUTDOWN: 'shutting down...',
    libvirt.VIR_DOMAIN_SHUTOFF:  'stopped',
    libvirt.VIR_DOMAIN_CRASHED:  'crashed',
    None: 'unknown',
}


@login_required
def instance_list(request):
    instances = []
    for i in Instance.objects.filter(owner=request.user):
        if i.active:
            try:
                c = libvirt.open(i.node.uri)
                dom = c.lookupByName(i.domain)
                info = dom.info()
            except:
                info = [None]
            finally:
                state = vm_state[info[0]]
        else:
            state = 'provisioning'
        instances += [{
            'db': i,
            'state': state,
        }]
    return render_to_response("limeade_cloud/instance_list.html", {
    "object_list": instances}, context_instance=RequestContext(request))


@login_required
def instance_add(request):
    form = InstanceForm(request.POST or None)
    form.fields['base_image'].choices = send_task("cloud.list_base_images", routing_key='limeade.cloud').get()
    form.fields['product'].queryset = Product.objects.filter(
        Q(owner=request.user.get_profile().parent) | Q(owner=request.user),
        limitset_cloud__isnull = False)
    form.fields['sshkeys'].queryset = SSHKey.objects.filter(owner=request.user)
    
    if form.is_valid():
        limits = form.cleaned_data['product'].limitset_cloud.get()
        node = get_best_node(limits.cpu_cores, limits.memory, limits.storage)
        if not node:
            messages.add_message(request, messages.ERROR, 'We are currently over capacity. Please try again soon.')
            return redirect('limeade_cloud_instance_list')
        
        i = Instance(hostname=form.cleaned_data['hostname'])
        i.node = node
        i.owner = request.user
        i.save() # generate a pk for the instance, so we can use the m2m field
        i.sshkeys = form.cleaned_data['sshkeys']
        i.generate_mac_addr()
        i.save()
        
        send_task("cloud.create_instance", kwargs = {
                'base_image': form.cleaned_data['base_image'],
                'cpu_cores':  limits.cpu_cores,
                'memory':     limits.memory,
                'storage':    limits.storage,
                'domain':     i.domain,
                'instance':   i.pk,
                'mac_addr':   i.mac_addr,
            }, routing_key='limeade.cloud')
        
        return redirect('limeade_cloud_instance_list')
    
    return render_to_response("limeade_cloud/instance_add.html",
        {"form": form}, context_instance=RequestContext(request))


@login_required
def instance_delete(request, slug):
    i = get_object_or_404(Instance, pk=slug)
    
    if i.owner == request.user:
        # TODO: send msg
        i.delete()
    
    return redirect('limeade_cloud_instance_list')


@login_required
def instance_start(request, slug):
    
    i = get_object_or_404(Instance, pk=slug)
    
    try:
        c = libvirt.open(i.node.uri)
        dom = c.lookupByName(i.domain)
        dom.create()
    except:
        # TODO: catch exception?
        pass
    
    return redirect('limeade_cloud_instance_list')


@login_required
def instance_stop(request, slug):
    i = get_object_or_404(Instance, pk=slug)
    
    try:
        c = libvirt.open(i.node.uri)
        dom = c.lookupByName(i.domain)
        dom.destroy()
    except:
        # TODO: catch exception?
        pass
    
    return redirect('limeade_cloud_instance_list')


@login_required
def instance_restart(request, slug):
    i = get_object_or_404(Instance, pk = slug)
    
    try:
        c = libvirt.open(i.node.uri)
        dom = c.lookupByName(i.domain)
        dom.destroy()
        dom.create()
    except:
        # TODO: catch exception?
        pass
    
    return redirect('limeade_cloud_instance_list')

