from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from limeade.system.utils import get_domains
from models import Account, Redirect
from forms import AccountForm, AccountEditForm, RedirectForm

# accounts 

@login_required
def account_list(request):
	domains = get_domains(request.user)
	return object_list(request, Account.objects.filter(domain__in = domains), template_name='limeade_mail/account_list.html')

@login_required
def account_add(request):
	form = AccountForm(request.POST or None)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_mail_account_list')
	return render_to_response("limeade_mail/account_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def account_edit(request, slug):
	account = Account.objects.get(pk=slug)
	form = AccountEditForm(request.POST or None, instance=account)
	if form.is_valid():
		form.save()
		return redirect('limeade_mail_account_list')
	return render_to_response("limeade_mail/account_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def account_delete(request, slug):
	# todo: permission checking
	get_object_or_404(Account, pk = slug).delete()
	return redirect('limeade_mail_account_list')
	
	
# redirects
@login_required
def redirect_list(request):
	domains = get_domains(request.user)
	return object_list(request, Redirect.objects.filter(domain__in = domains), template_name='limeade_mail/redirect_list.html')

@login_required
def redirect_add(request):
	form = RedirectForm(request.POST or None)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_mail_redirect_list')
	return render_to_response("limeade_mail/redirect_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def redirect_edit(request, slug):
	redirect = Redirect.objects.get(pk=slug)
	form = RedirectForm(request.POST or None, instance=redirect)
	form.fields['domain'].queryset = get_domains(request.user)
	if form.is_valid():
		form.save()
		return redirect('limeade_mail_redirect_list')
	return render_to_response("limeade_mail/redirect_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def redirect_delete(request, slug):
	# todo: permission checking
	get_object_or_404(Redirect, pk = slug).delete()
	return redirect('limeade_mail_redirect_list')	