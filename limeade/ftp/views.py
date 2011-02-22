from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from limeade.system.utils import get_domains
from limeade.web.models import VHost, get_vhosts
from models import Account
from forms import AccountForm, AccountEditForm

@login_required
def account_list(request):
	return object_list(request, Account.objects.filter(vhost__in=list(get_vhosts(request.user))),
			template_name='limeade_ftp/account_list.html')

@login_required
def account_add(request):
	form = AccountForm(request.POST or None)
	form.fields['vhost'].queryset = get_vhosts(request.user)
	if form.is_valid():
		ac = form.save(commit=False)
		ac.set_password(form.cleaned_data['password'])
		ac.save()
		return redirect('limeade_ftp_account_list')
	return render_to_response("limeade_ftp/account_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def account_edit(request, slug):
	account = Account.objects.get(pk=slug)
	if account.vhost.domain.owner() is not request.user:
		return redirect('limeade_ftp_account_list')
	form = AccountEditForm(request.POST or None, instance=account)
	if form.is_valid():
		ac = form.save(commit=False)
		ac.set_password(form.cleaned_data['password'])
		ac.save()
		return redirect('limeade_ftp_account_list')
	return render_to_response("limeade_ftp/account_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def account_delete(request, slug):
	ac = get_object_or_404(Account, pk = slug)
	if ac.vhost.domain.owner() == request.user:
		ac.delete()
	return redirect('limeade_ftp_account_list')
	
