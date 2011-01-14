from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from limeade.system.utils import get_domains
from models import VHost, HTTPRedirect as Redirect
from forms import VHostForm, VHostEditForm, RedirectForm

# accounts 

@login_required
def vhost_list(request):
	domains = get_domains(request.user)
	return object_list(request, VHost.objects.filter(domain__in = domains), template_name='limeade_web/vhost_list.html')

@login_required
def vhost_add(request):
	form = VHostForm(request.POST or None)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_web_vhost_list')
	return render_to_response("limeade_web/vhost_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def vhost_edit(request, slug):
	account = VHost.objects.get(pk=slug)
	form = VHostEditForm(request.POST or None, instance=account)
	if form.is_valid():
		form.save()
		return redirect('limeade_web_vhost_list')
	return render_to_response("limeade_web/vhost_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def vhost_delete(request, slug):
	# todo: permission checking
	get_object_or_404(VHost, pk = slug).delete()
	return redirect('limeade_web_vhost_list')
	
	
# redirects
@login_required
def redirect_list(request):
	domains = get_domains(request.user)
	return object_list(request, Redirect.objects.filter(domain__in = domains), template_name='limeade_web/redirect_list.html')

@login_required
def redirect_add(request):
	form = RedirectForm(request.POST or None)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_web_redirect_list')
	return render_to_response("limeade_web/redirect_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def redirect_edit(request, slug):
	redirect = Redirect.objects.get(pk=slug)
	form = RedirectForm(request.POST or None, instance=redirect)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_mail_redirect_list')
	return render_to_response("limeade_web/redirect_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def redirect_delete(request, slug):
	# todo: permission checking
	get_object_or_404(Redirect, pk = slug).delete()
	return redirect('limeade_web_redirect_list')	