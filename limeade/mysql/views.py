from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from celery.execute import send_task

from forms import DBForm, DBEditForm

@login_required
def db_list(request):
	# send sync list req
	return render_to_response("limeade_mysql/db_list.html",
		{"object_list": []}, context_instance = RequestContext(request))

@login_required
def db_add(request):
	form = DBForm(request.POST or None)
	if form.is_valid():
		# create
		return redirect('limeade_mysql_db_list')
	return render_to_response("limeade_mysql/db_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def db_edit(request, slug):

	form = DBEditForm(request.POST or None)
	if form.is_valid():
		# update pass
		return redirect('limeade_mysql_db_list')
	return render_to_response("limeade_mysql/db_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def db_delete(request, slug):
	# todo: permission checking
	#get_object_or_404(VHost, pk = slug).delete()
	
	return redirect('limeade_mysql_db_list')
	
