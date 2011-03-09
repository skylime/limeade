from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from django.http import HttpResponse
from anyjson import serialize
from limeade.system.models import Product
from models import Node, Instance, SSHKey
from forms import InstanceForm, SSHKeyForm
from utils import get_best_node
from celery.execute import send_task
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
	for i in Instance.objects.filter(owner = request.user):
		if i.active:
			try:
				c = libvirt.open(i.node.uri)
				dom = c.lookupByName(i.domain())
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
	return render_to_response("limeade_cloud/instance_list.html",
			{"object_list": instances}, context_instance = RequestContext(request))	

@login_required
def instance_add(request):
	
	form = InstanceForm(request.POST or None)
	form.fields['base_image'].choices = send_task("cloud.list_base_images", routing_key='limeade.cloud').get()
	form.fields['product'].queryset = Product.objects.filter(
		Q(owner = request.user.get_profile().parent) | Q(owner = request.user),
		limitset_cloud__isnull = False)
	form.fields['sshkeys'].queryset = SSHKey.objects.filter(owner = request.user)
	
	
	
	if form.is_valid():
		# manually enforce uniqueness (sqlite doesn't)
		if Instance.objects.filter(name = form.cleaned_data['name'], owner= request.user).exists():
			return
		
		
		limits = form.cleaned_data['product'].limitset_cloud.get()
		n = get_best_node(limits.cpu_cores, limits.memory, limits.storage)
		if not n:
			# fail better
			return
		i = Instance(
			name  = form.cleaned_data['name'],
			node  = n,
			owner = request.user
		)
		i.save()
		x = send_task("cloud.create_instance", kwargs={
				'base_image': form.cleaned_data['base_image'],
				'cpu_cores':  limits.cpu_cores,
				'memory':     limits.memory,
				'storage':    limits.storage,
				'name':       i.domain(),
				'instance':   i.pk,
			}, routing_key='limeade.cloud')
		return redirect('limeade_cloud_instance_list')
	return render_to_response("limeade_cloud/instance_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def instance_delete(request, slug):
	i = get_object_or_404(Instance, pk = slug)
	if i.owner == request.user:
		# send msg
		i.delete()
	return redirect('limeade_cloud_instance_list')

	
@login_required
def instance_start(request, slug):
	i = get_object_or_404(Instance, pk = slug)
	try:
		c = libvirt.open(i.node.uri)
		dom = c.lookupByName(i.domain())
		dom.create()
	except:
		pass	
	
	return redirect('limeade_cloud_instance_list')


@login_required
def instance_stop(request, slug):
	i = get_object_or_404(Instance, pk = slug)
	try:
		c = libvirt.open(i.node.uri)
		dom = c.lookupByName(i.domain())
		dom.destroy()
	except:
		pass
	
	return redirect('limeade_cloud_instance_list')


@login_required
def instance_restart(request, slug):
	i = get_object_or_404(Instance, pk = slug)
	try:
		c = libvirt.open(i.node.uri)
		dom = c.lookupByName(i.domain())
		dom.destroy()
		dom.create()
	except:
		pass	
	
	return redirect('limeade_cloud_instance_list')


# ssh keys
@login_required
def sshkey_list(request):
	return object_list(request, SSHKey.objects.filter(owner = request.user), template_name='limeade_cloud/sshkey_list.html')

@login_required
def sshkey_add(request):
	form = SSHKeyForm(request.POST or None)
	if form.is_valid():
		key = form.save(commit=False)
		key.owner = request.user
		key.save()
		return redirect('limeade_cloud_sshkey_list')
	return render_to_response("limeade_cloud/sshkey_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def sshkey_delete(request, slug):
	key = get_object_or_404(SSHKey, pk = slug)
	if key.owner == request.user:
		key.delete()
	return redirect('limeade_cloud_sshkey_list')


# API	
def instance_activate(request):
	if request.GET.get('site_api_key', '') != settings.SITE_API_KEY:
		return HttpResponse(serialize({"status": "failure", "reason": 'wrong key'}), mimetype="application/json")
	i = get_object_or_404(Instance, pk = request.GET['instance'])
	i.active = True
	i.save()
	response = {"status": "success", "retval": i.domain()}
	return HttpResponse(serialize(response), mimetype="application/json")
